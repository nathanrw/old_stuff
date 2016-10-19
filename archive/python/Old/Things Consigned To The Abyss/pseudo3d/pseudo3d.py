# Pseudo 3Dness ###############################################################
###############################################################################
#
#
#
###############################################################################

import pygame, math, random

        #[x,y,z]
points = [[0, 0, 0],
          [2, 0, 2],
          [0, 0, 4],
          [-2,0, 2],
          [0, 2, 0],
          [2, 2, 2],
          [0, 2, 4],
          [-2, 2, 2],
          ]

points2D = []

for set in points:
    points2D.append([set[0],set[1]])

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((400,400))

screen.fill((0xFF,0xFF,0xFF))
pygame.display.update()

dot = pygame.Surface((4,4))
dot.fill((0,0,0))


