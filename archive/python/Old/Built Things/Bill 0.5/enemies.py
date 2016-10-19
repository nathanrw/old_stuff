import os, random, pygame
from pygame.locals import *
from LoadRes import *

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, pos=None):
        pygame.sprite.Sprite.__init__(self)
        if pos is None: self.y = random.randrange(200,320,20)
        self.xvel = 2
        self.counter = 0
        self.limitcounter = 0
        self.state = "idle"
        self.shot = 0

class Flan(BaseEnemy):
    def __init__(self):
        return
    def update(self):
        return

class Cultists(BaseEnemy):
    def __init__(self, anim1, anim2):
        BaseEnemy.__init__(self)

        self.health = 1

        self.anim_walk = anim1
        self.anim_death = anim2
        self.image = self.anim_walk[0]
        self.rect = self.image.get_rect()

        self.rect.left = 800
        self.rect.bottom = self.y

        self.hitbox = [self.rect.left,
                       self.rect.right,
                       self.rect.top+123,
                       self.rect.bottom]
        
    def update(self):
        if self.state == "idle":
            if self.limitcounter == 2:
                self.image = self.anim_walk[self.counter]
                self.rect.move_ip(-self.xvel,0)
                if self.counter == 2:
                    self.counter = 0

                self.counter += 1
                
                self.limitcounter = 0

        self.limitcounter += 1
        if self.rect.right < 0:
            self.kill()

        if self.state == "dead":
            if self.limitcounter == 3:
                self.rect.move_ip(0,-8)
                self.image = self.anim_death[self.counter]
                if self.counter == 5:
                    self.kill()

                self.counter += 1
                
                self.limitcounter = 0

        self.hitbox = [self.rect.left,
                       self.rect.right,
                       self.rect.top+123,
                       self.rect.bottom]
        
    def destroy(self):
        self.state = "dead"
        self.counter = 0
        self.limitcounter = 0
        self.image = self.anim_death[0]

class CultTank(BaseEnemy):
    def __init__(self, anim1, anim2):
        BaseEnemy.__init__(self)
        self.state="idle"
        self.xvel = 9
        self.health = 3
        self.anim_move = anim1
        self.anim_death = anim2
        self.image = self.anim_move[0]
        self.rect = self.image.get_rect()

        self.rect.left = 800
        self.rect.bottom = self.y

        self.hitbox = [self.rect.left,
                       self.rect.right,
                       self.rect.top,
                       self.rect.bottom]
        self.holder = []

    def update(self):
        if self.state == "idle":
            self.rect.move_ip(-self.xvel,0)
            if self.limitcounter == 3:
                self.image = self.anim_move[self.counter]
                self.counter += 1
                if self.counter == 3:
                    self.counter = 0
                self.limitcounter = 0
            self.limitcounter += 1
            self.hitbox = [self.rect.left,
                           self.rect.right,
                           self.rect.top,
                           self.rect.bottom]
                
        if self.state == "dead":
            if self.limitcounter == 3:
                self.rect.move_ip(-self.xvel,0)
                self.image = self.anim_death[self.counter]
                self.counter += 1
                if self.counter == 7:
                    self.kill()
                
                self.limitcounter = 0
            self.limitcounter+=1
            
    def destroy(self):
        if self.health > 0:
            self.health -= 1
        elif self.health == 0:
            self.state = "dead"
            self.counter = 0
            self.limitcounter = 0
            self.holder = [self.rect.center,self.rect.bottom]
            self.image = self.anim_death[0]
            self.rect = self.image.get_rect()
            self.rect.center = self.holder[0]
            self.rect.bottom = self.holder[1] + 63

class SAB(BaseEnemy):
    def __init__(self, anim1, anim2=None):
        BaseEnemy.__init__(self)

        self.health = 1

        self.anim_walk = anim1
        self.image = self.anim_walk[0]
        self.rect = self.image.get_rect()

        self.rect.left = 800
        self.rect.bottom = self.y

        self.hitbox = [self.rect.left,
                       self.rect.right,
                       self.rect.top,
                       self.rect.bottom]

        self.shot = 0
        
    def update(self):
        if self.state == "idle":
            if self.limitcounter == 1:
                self.image = self.anim_walk[self.counter]
                self.rect.move_ip(-self.xvel,0)
                if self.counter == 7:
                    self.counter = 0
                if self.counter == 5: self.shot = 2
                elif self.counter == 0: self.shot = 1
                elif self.counter != 0 and self.counter != 5: self.shot = 0

                self.counter += 1
                
                self.limitcounter = 0

        self.limitcounter += 1
        if self.rect.right < 0:
            self.kill()

        if self.state == "dead":
            self.kill()

        self.hitbox = [self.rect.left,
                       self.rect.right,
                       self.rect.top,
                       self.rect.bottom]
        
    def destroy(self):
        self.state = "dead"
