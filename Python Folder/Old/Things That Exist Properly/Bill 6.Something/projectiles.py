#Projectiles.py
#Shots from the bastards trying to blow up your lord and master.

#Import py
import os, random, pygame
from pygame.locals import *
from LoadRes import *

#Other projectiles derived from this.
class BaseProjectile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, anim1, anim2=None):
        pygame.sprite.Sprite.__init__(self)
        
        self.counter = 0
        self.limitcounter = 0
        self.state = "idle"

        self.Anim_Fly = anim1
        if anim2 is not None: self.Anim_Splode = anim2
        self.image = self.Anim_Fly
        self.rect = self.image.get_rect()

        self.rect.left = xpos
        self.rect.top = ypos

        self.hitbox = [self.rect.left,
                       self.rect.right,
                       self.rect.top,
                       self.rect.bottom]

    def destroy(self):
        self.counter = 0
        self.limitcounter = 0
        self.state = "dead"

    def get_hitbox(self):
        self.hitbox = [self.rect.left,
                       self.rect.right,
                       self.rect.top,
                       self.rect.bottom]
    def checkgone(self):
        if self.rect.right < 0: self.kill()
        

class SAB_Plasma(BaseProjectile):
    def __init__(self, xpos, ypos, anim1, anim2=None):
        BaseProjectile.__init__(self, xpos, ypos, anim1, anim2=None)
        self.xvel = -30

    def update(self):
        if self.state == "idle": self.rect.move_ip(self.xvel,0)
        if self.state == "dead": self.kill()
        self.get_hitbox()
        self.checkgone()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, anim, xvel=0, yvel=0, angle=0, maxplays=1):
        pygame.sprite.Sprite.__init__(self)
        self.anim = anim
        self.image = self.anim[0]
        self.rect = self.image.get_rect()

        self.rect.left = pos[0]
        self.rect.top = pos[1]
        
        self.animlim = len(self.anim)-1

        self.limitcounter = 0
        self.counter = 0
        self.maxplays = maxplays
        self.playcounter = 0

        self.xvel = xvel
        self.yvel = yvel
    def update(self):
        if self.limitcounter == 2:
            self.image = self.anim[self.counter]
            self.rect.move_ip(self.xvel,self.yvel)
            self.counter += 1
            if self.counter == self.animlim:
                self.counter = 0
                self.playcounter += 1
            if self.playcounter == self.maxplays:
                self.kill()
            self.limitcounter = 0
        self.limitcounter += 1

class smoke(pygame.sprite.Sprite):
    def __init__(self,pos,anim):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = anim
        self.rect = self.image.get_rect()
        
        self.counter = 0
        self.limitcounter = 0
        self.rect.left = pos[0]
        self.rect.top = pos[1]
    def update(self):
        self.image = pygame.transform.rotate(self.image,15)
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        self.counter += 1
        if self.counter == 12:
            self.kill()

        
        
