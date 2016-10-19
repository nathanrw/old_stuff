#Import Modules
import os, pygame
from pygame.locals import *
from math import sin, cos, tan, asin, acos, atan, sqrt

#Import Game Files
from LoadRes import *
#Globals + Constants

TILESIZE = 16
SCREENRECT = (640,480)
allsprites = pygame.sprite.RenderUpdates()

class Screen():
    def __init__(self,SCREENRECT,title):
        pygame.display.init()
        self.display = pygame.display.set_mode((SCREENRECT), DOUBLEBUF)
        pygame.display.set_caption(str(title))
    def drawimage(self,image):
        pos = ((self.display.get_width()/2-image.get_width()/2),(self.display.get_height()/2-image.get_height()/2))
        self.display.fill((0,0,0))
        self.display.blit(image,(pos))
        pygame.display.flip()
    def destroy():
        pygame.display.quit()

def CONTROLLING():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            EXIT()
    return 1
            
def EXIT():
    pygame.quit()
    running = 0
    
def SHOWUPDATES():
    SCREEN.drawimage(DISPLAY)
    return

global SCREEN
SCREEN = Screen(SCREENRECT,"Window")

global DISPLAY
DISPLAY = pygame.Surface((400,400))

def main():
    pygame.init()
    running = 1
    while running == 1:
        if CONTROLLING() == 0:
            QUIT()
        DISPLAYUPDATES()
    return

if __name__ == '__main__': main()
    
