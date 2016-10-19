import pygame
import random
from random import *
from pygame.locals import *

#Base class for the squares.
class dot(pygame.sprite.Sprite):
    
    def __init__(self,tilesize):
        
        pygame.sprite.Sprite.__init__(self)

        #Randomises the type of the square.
        self.type = randrange(1,5)

        #Selects a random grid square.
        startpos = ((randrange(0,800/tilesize))*tilesize +20 - (tilesize/2)) , ((randrange(0,600/tilesize))*tilesize + 20 - (tilesize/2))

        #Colour based on type
        if self.type == 1:
            self.colour = (255,255,255)
        elif self.type == 2:
            self.colour = (0,255,255)
        elif self.type == 3:
            self.colour = (255,0,255)
        elif self.type == 4:
            self.colour = (255,255,0)

        #Creates the square image.
        self.image = pygame.Surface((tilesize/2,tilesize/2))
        self.image.fill((0,0,0))
        self.colimg = pygame.Surface((((tilesize/2)-2),((tilesize/2)-2)))
        self.colimg.fill(self.colour)
        self.image.blit(self.colimg,(1,1))

        #Square's rect
        self.rect = self.image.get_rect()
        self.rect.center = startpos

        #Speed = 0
        self.xmove = 0
        self.ymove = 0

        self.tile = ((startpos[0]-20)/tilesize,(startpos[1]-20)/tilesize)

        #Counter, update modifier and tilesize
        self.counter = 0
        self.movesperturn = 15
        self.tilesize = tilesize

        #Range of possible speeds.
        self.randomspeed = (-1,2)
        
    def update(self):

        #If the counter is less the the moves per turn, move
        if self.counter == 0:
            self.rect.move_ip(((self.xmove*self.tilesize),(self.ymove*self.tilesize)))
            self.counter = self.movesperturn
            self.xmove = 0
            self.ymove = 0

        #Reduce the counter by one so as to control the moves per turn.
        self.counter -= 1

        #If it goes off the grid, it goes around
        if self.rect.left < 20:
            self.rect.right = (820 - (self.tilesize/4))
        if self.rect.right > 820:
            self.rect.left = (20 + (self.tilesize/4))
        if self.rect.top < 20:
            self.rect.bottom = (620 - (self.tilesize/4))
        if self.rect.bottom > 620:
            self.rect.top = (20 + (self.tilesize/4))

        self.tile = ((self.rect.left-20)/self.tilesize,(self.rect.top-20)/self.tilesize)

#Deletes squares, based on the base square.
class reaper(dot):
    
    def __init__(self,tilesize):
        
        pygame.sprite.Sprite.__init__(self)

        startpos = ((randrange(0,800/tilesize))*tilesize +20 - (tilesize/2)) , ((randrange(0,600/tilesize))*tilesize + 20 - (tilesize/2))

        #'Tis black with a white border.
        self.image = pygame.Surface((tilesize/2,tilesize/2))
        self.image.fill((255,255,255))
        self.colimg = pygame.Surface((((tilesize/2)-2),((tilesize/2)-2)))
        self.colimg.fill((0,0,0))
        self.image.blit(self.colimg,(1,1))

        self.rect = self.image.get_rect()
        self.rect.center = startpos
        
        self.xmove = 0
        self.ymove = 0

        self.tile = ((startpos[0]-20)/tilesize,(startpos[1]-20)/tilesize)

        #3 times as fast as the normal square.
        self.counter = 0
        self.movesperturn = 5
        self.tilesize = tilesize

        self.randomspeed = (-1,2)
        
    def update(self):

        #If the counter is less the the moves per turn, move
        if self.counter == 0:
            self.xmove = randrange(self.randomspeed[0],self.randomspeed[1])
            self.ymove = randrange(self.randomspeed[0],self.randomspeed[1])
            self.rect.move_ip(((self.xmove*self.tilesize),(self.ymove*self.tilesize)))
            self.counter = self.movesperturn

        #Reduce the counter by one so as to control the moves per turn.
        self.counter -= 1

        #If it goes off the grid, kill it
        if self.rect.left < 20:
            self.rect.right = (820 - (self.tilesize/4))
        if self.rect.right > 820:
            self.rect.left = (20 + (self.tilesize/4))
        if self.rect.top < 20:
            self.rect.bottom = (620 - (self.tilesize/4))
        if self.rect.bottom > 620:
            self.rect.top = (20 + (self.tilesize/4))

        self.tile = ((self.rect.left-20)/self.tilesize,(self.rect.top-20)/self.tilesize)

