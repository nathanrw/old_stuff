import pygame; from pygame.locals import *
from functions import rotate_3D 
import math

global MOVING; MOVING = [0,0,0]

def accept_input(eventlist, Camera):
    #Events.
    for event in eventlist:

        #Exit.
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            return
        
        elif event.type == KEYDOWN:
                
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
                
            #Stop Moving.
            if event.key == K_w:
                MOVING[2] = 0
            if event.key == K_s:
                MOVING[2] = 0
            if event.key == K_d:
                MOVING[0] = 0
            if event.key == K_a:
                MOVING[0] = 0
                
    

    if pygame.mouse.get_pressed()[2]:

        A = 5
        A = 1/100.0
        
        ROTATE_Y, ROTATE_X = pygame.mouse.get_pos()
        ROTATE_Y -= Camera.size[0]/2.0
        ROTATE_X -= Camera.size[1]/2.0
        
        Camera.angle[0] += int(-ROTATE_X*A)
        Camera.angle[1] += int(-ROTATE_Y*A)

    V = 20

    if MOVING[0] == 1:
        Camera.position[2]+=V*math.sin(math.radians(Camera.angle[1]))
        Camera.position[0]+=V*math.cos(math.radians(Camera.angle[1]))
    elif MOVING[0] == -1:
        Camera.position[2]-=V*math.sin(math.radians(Camera.angle[1]))
        Camera.position[0]-=V*math.cos(math.radians(Camera.angle[1]))
    if MOVING[2] == 1:
        Camera.position[2]+=V*math.cos(math.radians(Camera.angle[1]))*math.cos(math.radians(Camera.angle[0]))
        Camera.position[0]-=V*math.sin(math.radians(Camera.angle[1]))*math.cos(math.radians(Camera.angle[0]))
        Camera.position[1]-=V*math.sin(math.radians(Camera.angle[0]))
    elif MOVING[2] == -1:
        Camera.position[2]-=V*math.cos(math.radians(Camera.angle[1]))*math.cos(math.radians(Camera.angle[0]))
        Camera.position[0]+=V*math.sin(math.radians(Camera.angle[1]))*math.cos(math.radians(Camera.angle[0]))
        Camera.position[1]+=V*math.sin(math.radians(Camera.angle[0]))

    return "nope"
