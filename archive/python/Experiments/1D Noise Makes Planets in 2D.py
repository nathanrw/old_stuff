#2D Planet Makey Thing

from random import random
from math import sin, cos, radians
import pygame
from pygame.locals import *

def Noise(x):
    x = (x<<13) ^ x;
    return ( 1.0 - ( (x * (x * x * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

def MakeCircle(radius, numpoints, magnitude):
    angleperpoint = 360.0/numpoints
    points = []
    for n in range(0,numpoints):
        rand = random()
        r = (Noise(int(n*rand*10))*magnitude + radius)
        points.append((r*cos(radians(n*angleperpoint)),r*sin(radians(n*angleperpoint))))
    return points

def DrawCircle(circle, pos, surf):
    ncirc = []
    for point in circle:
        ncirc.append((int(point[0])+surf.get_width()/2+pos[0],int(point[1])+surf.get_height()/2+pos[1]))
    pygame.draw.lines(surf,(255,255,255),1,ncirc,2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024,768))

    PlanetOne   = MakeCircle(200.0, 50, 15.0)
    PlanetTwo   = MakeCircle( 50.0, 25, 7.0 )
    PlanetThree = MakeCircle( 30.0, 18, 2.0 )
    PlanetFour  = MakeCircle( 10.0,  6, 1.0 )
    
    DrawCircle(PlanetOne,(100,100),screen)
    DrawCircle(PlanetTwo,(-300,100),screen)
    DrawCircle(PlanetThree,(100,-300),screen)
    DrawCircle(PlanetFour,(-100,-300),screen)

    while 1:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return

main()
