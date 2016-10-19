import pygame
from pygame.locals import *

def convert_3d_to_2d(coord, eye, screen):
    eye_to_screen = eye[2]-screen[2]
    eye_to_point = eye[2]-coord[2]
    if eye_to_screen < 0: eye_to_screen = -eye_to_screen
    if eye_to_point < 0: eye_to_point = -eye_to_point
    try:
        x = (coord[0] * eye_to_screen)/eye_to_point
        y = (coord[1] * eye_to_screen)/eye_to_point
    except ZeroDivisionError:
        return (0,0)

    return (x,y)

print convert_3d_to_2d((0,0,0),(0,0,0),(0,0,0))
    
