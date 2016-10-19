import threading
import pygame
import sys
import math
from pygame.locals import *
from vec2d import vec2d
from vec3d import vec3d

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    def reflected(self, normal):
        direction = ((2 * self.direction.dot(normal)/normal.dot(normal))*normal - self.direction)
        return Ray(self.origin, direction)

class Polygon():
    def __init__(self, position, world, points):
        self.points = points
        self.material = Material(0,1,(100,100,100))
        self.position = position
        self.world = world
        self.world.add(self)

    def calcAngleSum(self, Q, Points):
        i = 0
        anglesum = 0
        n = len(Points)
        while i < n:
            A = Points[i] - Q
            B = Points[(i+1)%n] - Q
            m1 = A.get_length()
            m2 = B.get_length()
            if m1*m2<=0.000001:
                return math.pi*2
            costheta = A.dot(B)/(m1*m2)
            try:anglesum += math.acos(costheta)
            except: pass
            i += 1
        return anglesum

    def collideRay(self, ray):
        relativeOrigin = ray.origin - self.position
        k = self.points[0].dot(self.normal)
        normalDotDirection = self.normal.dot(ray.direction)
        if not normalDotDirection:
            return None
        dist = (k - self.normal.dot(relativeOrigin))/normalDotDirection
        if dist < 0:
            return None
        intersection = relativeOrigin + dist * ray.direction
        threshold = 0.00000001
        anglesum = self.calcAngleSum(intersection, self.points)
        if (math.pi*2-threshold < anglesum) and (anglesum < math.pi*2+threshold):
            return ray.origin + dist * ray.direction
        return None
        
    def reflectRay(self, intersection, ray):
        reflectedRay = ray.reflected(self.normal)
        reflectedRay.origin = intersection
        return reflectedRay

    def refractRay(self, intersection, ray): pass

    def __getNormal(self):
        return (self.points[0].cross(self.points[1])).normalized()
    normal = property(fget=__getNormal)

class Light():
    def __init__(self, position, world, colour, brightness):
        self.position = position
        self.colour = colour
        self.brightness = brightness
        self.world = world
        self.world.add(self)
    
    def getLuminosity(self):
        R = self.colour[0]*self.brightness
        G = self.colour[1]*self.brightness
        B = self.colour[2]*self.brightness
        return R, G, B
    
    luminosity = property(fget = getLuminosity)

class Material():
    def __init__(self, transparency, reflectivity, colour):
        self.transparency = transparency
        self.reflectivity = reflectivity
        self.colour = colour

class Camera():
    def __init__(self, pos, rotation, dist):
        self.position = pos
        self.rotation = rotation
        self.dist = dist

class World():
    def __init__(self):
        self.__geometry = []
        self.lights = []
    
    def __getitem__(self, index):
        return self.__geometry[index]
    
    def add(self, item):
        if isinstance(item, Polygon):
            self.__geometry.append(item)
        elif isinstance(item, Light):
            self.lights.append(item)
    
    def remove(self, item):
        if isinstance(item, Polygon):
            self.__geometry.remove(item)
        elif isinstance(item, Light):
            self.lights.append(item)
        
    def collideRay(self, ray):
        nearestObject = None
        nearestDistance = 9999999999
        nearestIntersection = None
        for object in self.__geometry:
            intersection = object.collideRay(ray)
            if intersection:
                distance = (intersection - ray.origin).get_length()
                if distance < nearestDistance and intersection != ray.origin:
                    nearestObject = object
                    nearestDistance = distance
                    nearestIntersection = intersection
        if nearestObject:
            return nearestObject, nearestDistance, nearestIntersection
        return None, None, None
    
    def illuminate(self, point, colour):
        illumination = [0, 0, 0]
        for light in self.lights:
            ray = Ray(point, light.position-point)
            a, b, c = self.collideRay(ray)
            if not a:
                r = ray.direction.get_length()
                inv_r_squared = 1.0/(r*r)
                illumination[0] += light.luminosity[0]*inv_r_squared
                illumination[1] += light.luminosity[1]*inv_r_squared
                illumination[2] += light.luminosity[2]*inv_r_squared
        R = colour[0] * illumination[0]
        G = colour[1] * illumination[1]
        B = colour[2] * illumination[2]
        return R, G, B
        
    def escapedRayColour(self, ray):
        y = ray.direction.normalized().y
        return (-100*y+20,-120*y+20,-200*y+40)
        
class ThreadedFiller():
    def __init__(self, numThreads, surface):
        for n in range(0, numThreads):
            f = FillerThread(n, numThreads, surface)
            f.start()
            
class Raytracer():
    def __init__(self, numThreads, surface, world, camera):
        self.numThreads = numThreads
        self.surface = surface
        self.world = world
        self.camera = camera
        
        self.w = self.surface.get_width()
        self.h = self.surface.get_height()
        
        self.maxRecursionDepth = 16
        
    def start(self):
        for n in range(0, self.numThreads):
            f = FillerThread(n, self.numThreads, self.surface, self.trace)
            f.start()
    
    def trace(self, x, y):

        origin = self.camera.position
        
        direction = vec3d( x - self.w/2,
                           y - self.h/2,
                           self.camera.dist )
                           
        direction.rotate_around_x(math.degrees(self.camera.rotation[0]))
        direction.rotate_around_y(math.degrees(self.camera.rotation[1]))
        direction.rotate_around_z(math.degrees(self.camera.rotation[2]))
        
        return self.castRay(Ray(origin, direction))
    
    def castRay(self, ray, recursionDepth=0):
        
        if recursionDepth > self.maxRecursionDepth:
            return self.world.escapedRayColour(ray)
        
        nearestObject, nearestDistance, intersection = self.world.collideRay(ray)
        
        if not nearestObject:
            return self.world.escapedRayColour(ray)
        
        baseColour = nearestObject.material.colour
        litColour = self.world.illuminate(intersection, baseColour)
        
        reflectionColour = (0,0,0)
        refractionColour = (0,0,0)
        
        if nearestObject.material.reflectivity:
            reflectedRay = nearestObject.reflectRay(intersection, ray)
            reflectionColour = self.castRay(reflectedRay, recursionDepth)
        
        if nearestObject.material.transparency:
            refractedRay = nearestObject.refractRay(intersection, ray)
            refractionColour = self.castRay(refractedRay, recursionDepth)
        
        k1 = nearestObject.material.transparency
        k2 = nearestObject.material.reflectivity
        
        R = litColour[0] + reflectionColour[0]*k2 + refractionColour[0]*k1
        G = litColour[1] + reflectionColour[1]*k2 + refractionColour[1]*k1
        B = litColour[2] + reflectionColour[2]*k2 + refractionColour[2]*k1
        
        return R, G, B
        
class FillerThread(threading.Thread):

    def __init__(self, threadNo, numThreads, surface,
                 colour_func = lambda x, y: (255,255,0)):
        threading.Thread.__init__(self)
        
        self.w = surface.get_width()
        self.h = surface.get_height()
        
        self.x = threadNo % self.w
        self.y = threadNo / self.h
        
        self.step = numThreads
        self.surface = surface
        
        self.colour_func = colour_func
    
    def capNumber(self, num, range):
        if num > range[1]: num = range[1]
        if num < range[0]: num = range[0]
        return num
    
    def capColour(self, col):
        return ( self.capNumber(col[0],(0,255)),
                 self.capNumber(col[1],(0,255)),
                 self.capNumber(col[2],(0,255)) )
        
    def run(self):
        while self.y < self.h:
            colour = self.colour_func(self.x, self.y)
            cappedColour = self.capColour(colour)
            self.surface.set_at((self.x,self.y),cappedColour)
            self.x += self.step 
            if self.x >= self.w:
                self.x = self.x - self.w
                self.y += 1

def main():
    pygame.init()
    screen = pygame.display.set_mode((200,200))
    surf = screen.copy()
    
    world = World()
    
    Polygon(vec3d(0,0,100),world, [vec3d(-100,100,0),vec3d(100,100,10),vec3d(100,-100,0),vec3d(-100,-100,0)])
    Polygon(vec3d(0,0,0),world, [vec3d(-100,-100,-100),vec3d(-100,-100,100),vec3d(-100,100,100),vec3d(-100,100,-100)])
    #Polygon(vec3d(0,0,100),world, [])
    #Polygon(vec3d(0,0,100),world, [])
    #Polygon(vec3d(0,0,100),world, [])
    
    Light(vec3d(100,0,-200), world, (100,100,100), 500)
    camera = Camera(vec3d(0,0,-200), [0,0,0], 50)
    
    rt = Raytracer(30, surf, world, camera)
    rt.start()
    while 1:
        screen.blit(surf, (0,0))
        pygame.display.update()
        for e in pygame.event.get(): pass
        
if __name__ == '__main__':
    try:
        main()
    except:
        print sys.excepthook(*sys.exc_info())
        w = raw_input()