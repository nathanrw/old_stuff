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
        self.xvel = -10

    def update(self):
        if self.state == "idle": self.rect.move_ip(self.xvel,0)
        if self.state == "dead": self.kill()
        self.get_hitbox()
        self.checkgone()
