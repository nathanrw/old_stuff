import constants
import maths2D
import math
import pygame
import random

class Body():

    colour = (255, 175, 150)

    def __init__(self, position, velocity, mass, radius, *groups):

        self.Px = position[0]
        self.Py = position[1]

        self.Vx = velocity[0]
        self.Vy = velocity[1]

        self.mass = mass

        self.radius = radius

        self.inshadow = 0

        self.groups = []
        for group in groups:
            self.groups.append(group)
            group.append(self)

    def fall(self, body):

        displacement = maths2D.sub2D(self.getPosition(), body.getPosition())

        r = maths2D.distance2D(displacement)
        direction = maths2D.normalise2D(displacement)

        # g = GM/r^2
        g = -constants.G*body.getMass()/(r*r)

        self.accelerate(maths2D.scale2D(direction, g))

    def calculateShadow(self, screenrect):
        
        axis = maths2D.normalise2D(self.getPosition())
        axis2 = (-axis[1], axis[0])

        r = maths2D.scale2D(axis2, -self.getRadius())

        A = maths2D.add2D(self.getPosition(), r)
        B = maths2D.sub2D(self.getPosition(), r)

        A = maths2D.add2D(A, maths2D.scale2D(axis, 2))
        B = maths2D.add2D(B, maths2D.scale2D(axis, 2))

        axis_A = maths2D.normalise2D(A)
        axis_B = maths2D.normalise2D(B)

        A = maths2D.add2D(A, (screenrect.w/2, screenrect.h/2))
        B = maths2D.add2D(B, (screenrect.w/2, screenrect.h/2))

        D = maths2D.add2D(A, maths2D.scale2D(axis_A, 900))
        C = maths2D.add2D(B, maths2D.scale2D(axis_B, 900))

        return A, B, C ,D

    def calculateLineToEdgeOfScreen(self, pos, dir, screenrect):

        if dir[0] < 0:
            x = 0

        elif dir[0] > 0:
            x = screenrect.w
        else:
            x = None
            const_x = None

        if x:
            const_x = (x - pos[0])/dir[0]

        if dir[1] < 0:
            y = 0
        elif dir[1] > 0:
            y = screenrect.h
        else:
            y = None
            const_y = None

        if y:
            const_y = (x - pos[1])/dir[1]

        if abs(const_x) < abs(const_y):
            return maths2D.add2D(pos, maths2D.scale2D(dir, const_x))

        else:
            return maths2D.add2D(pos, maths2D.scale2D(dir, const_y))

    def calculateOrbitalVelocity(self, body):

        displacement = maths2D.sub2D(self.getPosition(), body.getPosition())

        r = maths2D.distance2D(displacement)
        direction = maths2D.normalise2D(displacement)

        #GmM/r^2 = mv^2/r
        speed = math.sqrt(constants.G*body.mass/r)

        return -direction[1]*speed, direction[0]*speed

    def accelerate(self, accel):
        self.Vx += accel[0]
        self.Vy += accel[1]

    def getPosition(self):
        return self.Px, self.Py

    def getPositionPolar(self):
        r = maths2D.distance2D(self.getPosition())
        theta = math.atan2(self.getPosition())

        return r, theta

    def getVelocity(self):
        return self.Vx, self.Vy

    def destroy(self):
        for group in self.groups:
            if self in group:
                group.remove(self)

    def addGroup(self, group):
        if not self in group:
            group.append(self)

    def draw(self, surface):
        pos = maths2D.add2D(self.getPosition(), maths2D.scale2D(surface.get_rect().size, 0.5))
        try:
            pygame.draw.circle(surface, self.colour, pos, self.radius, 2)
        except:
            pygame.draw.circle(surface, self.colour, pos, self.radius)

    def getMass(self):
        return self.mass

    def getRadius(self):
        return self.radius

    def update(self):
        self.Px += self.Vx
        self.Py += self.Vy

    def setVelocity(self, velocity):
        self.Vx = velocity[0]
        self.Vy = velocity[1]

    def collide(self, body):
        dist = maths2D.distance2D(maths2D.sub2D(self.getPosition(), body.getPosition()))
        if dist < self.getRadius()+body.getRadius():
            self.handle_collide(body)
            return 1
        return 0

class Sun(Body):

    colour = (255, 255, 0)

    def __init__(self, mass, radius, *groups):
        Body.__init__(self, (0,0), (0,0), mass, radius, *groups)

    def handle_collide(self, body):
        body.destroy()

class Asteroid(Body):

    def __init__(self, position, velocity, mass, radius, *groups):
        Body.__init__(self, position, velocity, mass, radius, *groups)

    def handle_collide(self, body):

        if isinstance(body, Asteroid):

            m = self.getMass() + body.getMass()
            r = self.getRadius() + body.getRadius()
            fractions = random.randrange(3, 5)
            m_step = m/fractions
            r_step = r/fractions

            for x in range(0, fractions):

                theta = random.random()*math.pi*2

                sintheta = math.sin(theta)
                costheta = math.cos(theta)

                displacement = (self.radius+20)*sintheta, (self.radius+20)*costheta
                acceleration = sintheta, costheta

                pos = maths2D.add2D(self.getPosition(), displacement)
                vel = maths2D.add2D(self.getVelocity(), acceleration)

                Asteroid(pos, vel, m_step, r_step, *self.groups)

            body.destroy()
            self.destroy()

        elif isinstance(body, Sun):
            self.destroy()

        elif isinstance(body, Lettuce):
            body.destroy()

class Lettuce(Body):

    colour = (100, 255, 100)

    def __init__(self, position, velocity, mass, radius, *groups):
        Body.__init__(self, position, velocity, mass, radius, *groups)

    def handle_collide(self, body):

        if isinstance(body, Lettuce):
            body.destroy()
            self.destroy()
        else:
            self.destroy()

    def update(self):
        Body.update(self)
        if not self.inshadow:
            self.radius += constants.Meter * 1000
            self.mass += constants.Kilogram * 1000
            self.colour = (100, 255, 100)
        else:
            self.colour = (255, 255, 100)