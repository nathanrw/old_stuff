#'Tis a program. Yes.

import pygame, math, os
from pygame.locals import *

#Stuff

#Main

def main():

    running = 1
    drawing = 0

    screen = pygame.display.set_mode((800,600), DOUBLEBUF)
    screen.fill((255,255,255))
    pygame.display.flip()

    dot = pygame.Surface((1,1))
    dot.fill((0,0,0))

    while running:
        
        mpos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == K_ESCAPE:
                running = 0
            elif event.type == MOUSEBUTTONDOWN:
                drawing = 1
            elif event.type == MOUSEBUTTONUP:
                drawing = 0
            elif event.type == K_c:
                screen.fill((255,255,255))

        if drawing == 1:
            screen.blit(dot,mpos)

        pygame.display.flip()

    pygame.time.delay(10)

    pygame.image.save(screen, "pict.bmp")
    
    print "Have a nice day."
    return

#Run it all

if __name__ == '__main__': main()
