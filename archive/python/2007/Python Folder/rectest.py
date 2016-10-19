import pygame, os, math
from pygame.locals import *

def square():
    image = pygame.Surface((30, 30))
    pygame.draw.rect(image, (200, 200, 200), (0, 0, 20, 20), 0)
    return image.convert()

def main():
    
    pygame.init()  
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("hmm")
    jeff = square()
    screen.blit(jeff, (30, 30))
    
    pygame.display.update()
    pygame.display.flip()

    running = 1
    
    while running == 1:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0

main()
