import pygame
from pygame.locals import *
from math import *
import shapes

pygame.font.init()

WINDOW_SIZE = (1200,900)
ROTATING = [0,0,0] #In what ways the camera is rotating.
MOVING = [0,0,0] #In what ways the camera is moving.
FONT = pygame.font.Font(None, 18) #Used to display framerate and the like.
CLOCK = pygame.time.Clock()

CAMERA_VELOCITY = (0,0,0)

def rotation(a,angle,b=(0,0,0)):
    #Rotate the average about the origin and then add b to it.

    #Put the angle in radians, then calculate sine and cosine of it.
    angle = radians(angle)
    sinval = sin(angle)
    cosval = cos(angle)

    #Make about origin.
    average_A_axis = a[0] - b[0]
    average_B_axis = a[1] - b[1]

    #Rotate + translate.
    nA = (average_A_axis * cosval - average_B_axis * sinval) + b[0]
    nB = (average_A_axis * sinval + average_B_axis * cosval) + b[1]

    return (nA,nB)

def rotate_camera_movement(point, angle):
    #Rotate the movement vector thing so that the camera moves
    #relative to which way it is looking.

    #Rotate x and z coordinates about y axis.
    xz = rotation((point[0],point[2]),angle[1])
    #Rotate y and z coordinates about x axis.
    yz = rotation((point[1],xz[1]),angle[0])
    #Rotate x and y coordinates about z axis.
    xy = rotation((xz[0],yz[0]),angle[2])

    #Vector rotated. Yeah.
    return (xy[0],xy[1],yz[1])

class camera():
    #Why this is all in this class, none can tell...
    #iSee
    def __init__(self, window):
        self.position = [0,0,0]
        self.angle = [0,0,0]
        self.field_of_view = (0,0,0)
        self.dist_to_screen = 200
        self.windowsize = window
        self.surface = pygame.Surface((window[0],window[1]))
        self.surface.fill((0,0,0))
        self.dot = pygame.Surface((3,3))
        self.dot.fill((255,255,255))
        self.points = []
        self.polygons = []
        self.rounded_points = []
        self.cube = shapes.CreateCube(10,(0,0,50))

    def transform_point(self,point):
        #point[0]-self.position[0] makes the camera the origin.
        #Angle is made negative to get it to go in the right direction.
        #The 3d coordinates are rotated about the eye and then changed into 2d coordinates.
        try:
            xyz = rotate_camera_movement((point[0]-self.position[0], point[1]-self.position[1], point[2]-self.position[2]),
                                         (-self.angle[0], -self.angle[1], -self.angle[2])
                                         )
            
            return((self.dist_to_screen/xyz[2])*xyz[0] + self.windowsize[0]/2,
                   (self.dist_to_screen/xyz[2])*xyz[1] + self.windowsize[1]/2)
        except ZeroDivisionError:
            return (self.windowsize[0]/2,self.windowsize[1]/2)
        
    def transform_points(self, points):
        for point in points:
            self.points.append(self.transform_point(point))

    def draw_shape(self,shape):
        self.surface.fill((0,0,0))
        polygons = []
        for polygon in shape:
            polygons.append(polygon.add())
        newpolies = []
        for polygon in polygons:
            pygame.draw.lines(self.surface,(255,255,255),1,transform_points(polygon),2)
            
    def draw_lines(self):
        #Draw the test prism thing.
        self.surface.fill((0,0,0))
        self.rounded_points = []
        for point in self.points:
            self.rounded_points.append((int(point[0]),int(point[1])))
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[0],
                         self.rounded_points[1],2)
        except:pass
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[1],
                         self.rounded_points[2],2)
        except:pass
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[2],
                         self.rounded_points[3],2)
        except:pass
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[3],
                         self.rounded_points[0],2)
        except:pass
        ###
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[4],
                         self.rounded_points[5],2)
        except:pass
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[5],
                         self.rounded_points[6],2)
        except:pass
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[6],
                         self.rounded_points[7],2)
        except:pass
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[7],
                         self.rounded_points[4],2)
        except:pass
        ###
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[4],
                         self.rounded_points[0],2)
        except:pass
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[5],
                         self.rounded_points[1],2)
        except:pass
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[6],
                         self.rounded_points[2],2)
        except:pass
        try:pygame.draw.line(self.surface,(255,255,255),
                         self.rounded_points[7],
                         self.rounded_points[3],2)
        except:pass
    
    def return_surface(self):
        #WASTED SPACE IS WASTED
        return self.surface

    def move(self,CAMERA_VELOCITY):
        self.position = move_point(self.position,rotate_camera_movement(CAMERA_VELOCITY,self.angle))
    
    def update_view(self, points):
        #Draw stuff to the camera.
        newangle = []

        #Stop the angle from going batshit insane.
        for theta in self.angle:
            if theta >= 360: theta = 0
            elif theta <= -360: theta = 0
            newangle.append(theta)
        self.angle = newangle

        #2D-atise the points
        self.points = []
        self.transform_points(points)
        
        #Draw the points.
        self.draw_lines()

def move_point(a,b):
    #Obv.
    return (a[0]+b[0],a[1]+b[1],a[2]+b[2])

def pointsgen(counter):
    #Crazy shit.
    counter = radians(counter)
    points = []
    points.append((-50*sin(counter),50*sin(counter),50*sin(counter)+50))
    points.append((50*sin(counter),50*sin(counter),50*sin(counter)+50))
    points.append((50*sin(counter),-50*sin(counter),50*sin(counter)+50))
    points.append((-50*sin(counter),-50*sin(counter),50*sin(counter)+50))
    points.append((-50*sin(counter),50*sin(counter),50*sin(counter)+110))
    points.append((50*sin(counter),50*sin(counter),50*sin(counter)+110))
    points.append((50*sin(counter),-50*sin(counter),50*sin(counter)+110))
    points.append((-50*sin(counter),-50*sin(counter),50*sin(counter)+110))
    return points
    
def main():
    
    #Fire up zee pygame.
    pygame.init()
    
    #The surface that gets displayed.
    screen = pygame.display.set_mode(WINDOW_SIZE,DOUBLEBUF)
    pygame.display.set_caption("A Program That Shows A Rectangular Prism. Yay.")
    
    #The test cube.
    points = ((-50,50,60),(50,50,60),(50,-50,60),(-50,-50,60),
              (-50,50,100),(50,50,100),(50,-50,100),(-50,-50,100))
    
    Camera = camera(WINDOW_SIZE) #Make a camera.
    counter = 0 #Keeps track of something or other.
    sinner = 0.0 #Makes the crazy oscillations.

    #Main loop.
    while 1:
        
        #Events.
        for event in pygame.event.get():

            #Exit.
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            
            elif event.type == KEYDOWN:
                #Rotation
                if event.key == K_j: #+Y
                    ROTATING[1] = 1
                if event.key == K_i: #+X
                    ROTATING[0] = 1
                if event.key == K_l: #-Y
                    ROTATING[1] = -1
                if event.key == K_k: #-X
                    ROTATING[0] = -1
                if event.key == K_o: #+Z
                    ROTATING[2] = 1
                if event.key == K_p: #-Z
                    ROTATING[2] = -1

                if event.key == K_m: #Reset z rotation.
                    Camera.angle = (Camera.angle[0],
                                    Camera.angle[1],
                                    0)
                    
                #Translation
                if event.key == K_w: #Forward
                    MOVING[2] = 1
                if event.key == K_s: #Backward
                    MOVING[2] = -1
                if event.key == K_d: #Right
                    MOVING[0] = 1
                if event.key == K_a: #Left
                    MOVING[0] = -1
                    
            if event.type == KEYUP:
                
                #Stop rotation
                if event.key == K_j:
                    ROTATING[1] = 0
                if event.key == K_i:
                    ROTATING[0] = 0
                if event.key == K_l:
                    ROTATING[1] = 0
                if event.key == K_k:
                    ROTATING[0] = 0
                if event.key == K_o:
                    ROTATING[2] = 0
                if event.key == K_p:
                    ROTATING[2] = 0
                    
                #Stop Moving.
                if event.key == K_w:
                    MOVING[2] = 0
                if event.key == K_s:
                    MOVING[2] = 0
                if event.key == K_d:
                    MOVING[0] = 0
                if event.key == K_a:
                    MOVING[0] = 0
                    
        #Rotate the camera.
        if ROTATING[0] == 1:
            Camera.angle[0] += 1
        elif ROTATING[0] == -1:
            Camera.angle[0] -= 1
        if ROTATING[1] == 1:
            Camera.angle[1] += 1
        elif ROTATING[1] == -1:
            Camera.angle[1] -= 1
        if ROTATING[2] == 1:
            Camera.angle[2] += 1
        elif ROTATING[2] == -1:
            Camera.angle[2] -= 1

        #Translate the camera.
        if MOVING[0] == 1:
            CAMERA_VELOCITY = (1,0,0)
            Camera.move(CAMERA_VELOCITY)
        elif MOVING[0] == -1:
            CAMERA_VELOCITY = (-1,0,0)
            Camera.move(CAMERA_VELOCITY)
        if MOVING[2] == 1:
            CAMERA_VELOCITY = (0,0,1)
            Camera.move(CAMERA_VELOCITY)
        elif MOVING[2] == -1:
            CAMERA_VELOCITY = (0,0,-1)
            Camera.move(CAMERA_VELOCITY)
            
        #Oscillate.
        #points = pointsgen(sinner)
        sinner += 1
        
        #Take a picture.
        Camera.update_view(points)
        
        #Draw the camera's view to the screen.
        screen.blit((Camera.return_surface()),(0,0))
        
        #Draw text.
        screen.blit(FONT.render("FPS: " + str(int(CLOCK.get_fps())),1,(250,250,250)),(5,5))
        screen.blit(FONT.render("Camera Position: " + str(Camera.position),1,(250,250,250)),(5,30))
        screen.blit(FONT.render("Camera Rotation: " + str(Camera.angle),1,(250,250,250)),(5,55))
        screen.blit(FONT.render("WASD to move, IJKL to rotate about x and y,",1,(250,250,250)),(5,80))
        screen.blit(FONT.render("OP to rotate about z, and m to reset z rotation.",1,(250,250,250)),(5,105))
        
        #Update the screen.
        pygame.display.update()
        
        #Count.
        counter += 1
        
        #Sine does one oscillation for every pi/2 radians. Crazy shit
        #tends to happen if this is, say, twenty-seven.
        if sinner >= 180:
            sinner = 0
            
        #Keep it at 60 FPS.
        CLOCK.tick(60)

main()
pygame.quit()

    
