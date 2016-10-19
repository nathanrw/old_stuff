import os, random, pygame, math
from pygame.locals import *
from LoadRes import *

random.seed()

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, pos=None):
        pygame.sprite.Sprite.__init__(self)
        if pos is None:
            self.y = random.randrange(200,320,20)
            self.xvel = 2
        if pos is not None:
            self.y = pos[0]
            self.x = pos[1]
            self.xvel = 0
            self.yvel = 0
            self.angle = 0

        self.name = ""
        self.counter = 0
        self.limitcounter = 0
        self.state = "idle"
        self.shot = 0
        
    def getbox(self):
        self.hitbox = [self.rect.left,
                       self.rect.right,
                       self.rect.top,
                       self.rect.bottom]

class RaRaRasputin(BaseEnemy):
    def __init__(self,anim1):
        BaseEnemy.__init__(self, (800,180))
        
        self.name = "rasputin"

        self.health = 200
        self.anim_walk = anim1
        self.anim_stunned = []
        for img in anim1:
            self.anim_stunned.append(pygame.transform.rotate(img,30))
        self.image = self.anim_walk[0]
        self.rect = self.image.get_rect()

        self.rect.left = self.x
        self.rect.bottom = self.y

        self.state = "rasputin_idle"
        self.getbox()

        self.stuncount = 0
        self.stuntime = 0
        self.hitcount = 0

    def update(self):
        if self.health < 0:
            self.kill()

        if self.state == "rasputin_idle":
            if self.limitcounter == 2:
                self.image = self.anim_walk[self.counter]
                self.counter += 1
                self.velchange()
                self.bouncer()
                self.rect.move_ip(self.xvel,self.yvel)
                
                if self.counter > len(self.anim_walk)-1:
                    self.counter = 0
                self.limitcounter = 0

                if self.stuncount >= 40:
                    self.stun()

        if self.state == "rasputin_stunned":
            if self.limitcounter == 2:
                self.image = self.anim_stunned[self.counter]
                self.counter += 1
                self.stuntime += 1
                if self.hitcount > 50:
                    self.unstun()
                if self.rect.bottom < 300:
                    self.rect.move_ip(0,2)
                if self.counter > len(self.anim_stunned)-1:
                    self.counter = 0
                self.limitcounter = 0

        self.limitcounter += 1
        self.getbox()

    def destroy(self):
        if self.state == "rasputin_stunned":
            self.health -= 1
            self.hitcount += 1

            if self.hitcount == 200:
                self.unstun()
        elif self.state == "rasputin_idle":
            self.hit()

    def stun(self):
        self.stuncount = 0
        self.state = "rasputin_stunned"
        oldcentre = self.rect.center
        self.image = self.anim_stunned[0]
        self.rect = self.image.get_rect()
        self.rect.center = oldcentre

    def unstun(self):
        self.hitcount = 0
        self.state = "rasputin_idle"

    def hit(self):
        self.stuncount += 1

    def velchange(self):
        self.xvel += random.randrange(-2,3,1)
        self.yvel += random.randrange(-2,3,1)

        if self.xvel > 5 or self.xvel < -5:
            self.xvel += -self.xvel
        if self.yvel > 5 or self.yvel < -5:
            self.yvel += -self.yvel

        if self.rect.left < 300:
            self.xvel += 2

    def bouncer(self):
        if self.rect.top < 60:
            self.rect.top = 60
            self.yvel = -self.yvel
        if self.rect.bottom > 320:
            self.rect.bottom = 320
            self.yvel = -self.yvel
        if self.rect.left < 0:
            self.rect.left = 0
            self.xvel = -self.xvel
        if self.rect.right > 800:
            self.rect.right = 800
            self.xvel = -self.xvel

class Cultists(BaseEnemy):
    def __init__(self, anim1, anim2):
        BaseEnemy.__init__(self)

        self.name = "Cultists"
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

        self.name = "Tank"
        self.state="idle"
        self.xvel = 9
        self.health = 3
        self.anim_move = anim1
        self.anim_death = anim2
        self.image = self.anim_move[0]
        self.rect = self.image.get_rect()

        self.rect.left = 800
        self.rect.bottom = self.y

        self.getbox()
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
    def __init__(self, anim1, anim2=None, anim3=None):
        BaseEnemy.__init__(self)

        self.name = "SAB"
        self.health = 1

        self.anim_walk = anim1
        self.anim_shoot = anim1
        self.image = self.anim_walk[0]
        self.rect = self.image.get_rect()

        self.rect.left = 800
        self.rect.bottom = self.y

        self.getbox()

        self.shot = 0
        self.gun = [29,24]
        self.shootercounter = 0
        self.gunmodifier = -10
        
    def update(self):
        if self.state == "idle":
            if self.limitcounter == 1:
                self.image = self.anim_walk[self.counter]
                self.rect.move_ip(-self.xvel,0)
                if self.counter == 7:
                    self.counter = 0
                self.counter += 1
                self.limitcounter = 0
            if self.shootercounter == 14:
                self.shootercounter = 0
                self.shoot()
            self.shootercounter += 1
            
        if self.state == "shooting":
            if self.limitcounter == 1:
                self.image = self.anim_shoot[self.counter]
                self.rect.move_ip(-self.xvel,0)
                if self.counter == 5: self.shot = 2
                elif self.counter == 0: self.shot = 1
                elif self.counter != 0 and self.counter != 5: self.shot = 0
                self.counter += 1
                self.limitcounter = 0
            if self.counter == 7:
                self.idle()

        self.limitcounter += 1

        if self.state == "dead":
            self.kill()

        self.getbox()
        
    def destroy(self):
        self.state = "dead"

    def shoot(self):
        self.state = "shooting"
        self.counter = 0
        self.limitcounter = 0
        self.image = self.anim_shoot[0]

    def idle(self):
        self.state = "idle"
        self.counter = 0
        self.limitcounter = 0
        self.image = self.anim_walk[0]
        self.shot = 0

class Gatling(BaseEnemy):
    def __init__(self, anim1, anim2=None, anim3=None):
        BaseEnemy.__init__(self)

        self.name = "Gatling"
        self.health = 1
        self.xvel = 1.25

        self.anim_walk = anim1
        self.anim_shoot = anim1
        self.anim_die = anim2
        self.image = self.anim_walk[0]
        self.rect = self.image.get_rect()

        self.rect.left = 800
        self.rect.bottom = self.y

        self.getbox()

        self.shot = 1
        self.gun = [29]
        self.shootercounter = 0
        self.hot = 0
        self.gunmodifier = -10

        self.state = "shooting"
        
    def update(self):
        if self.state == "idle":
            self.shot = 0
            if self.limitcounter == 1:
                self.image = self.anim_walk[self.counter]
                self.rect.move_ip(-self.xvel,0)
                if self.counter == 7:
                    self.counter = 0
                    self.shootercounter += 1
                self.counter += 1
                self.limitcounter = 0
                if self.shootercounter == 7:
                    self.state = "shooting"
                    self.shootercounter = 0
            
        if self.state == "shooting":
            if self.limitcounter == 1:
                self.image = self.anim_shoot[self.counter]
                self.rect.move_ip(-self.xvel,0)
                if self.counter == 0:
                    self.shot = 1
                    self.gun[0] = 29
                elif self.counter == 2:
                    self.shot = 1
                    self.gun[0] = 27
                elif self.counter == 4:
                    self.shot = 1
                    self.gun[0] = 34
                elif self.counter == 6:
                    self.shot = 1
                    self.gun[0] = 26
                elif self.counter != 0 \
                     and self.counter != 2 \
                     and self.counter != 4 \
                     and self.counter != 6: self.shot = 0
                self.counter += 1
                self.limitcounter = 0
            if self.counter == 7:
                self.counter = 0
                self.hot += 1

        if self.state == "dead":
            self.kill()

        if self.hot == 10:
            self.state = "idle"
            self.hot = 0

        self.limitcounter += 1

        self.getbox()
        
    def destroy(self):
        self.state = "dead"
        self.counter = 0
        self.limitcounter = 0

    def idle(self):
        self.state = "idle"
        self.counter = 0
        self.limitcounter = 0
        self.image = self.anim_walk[0]
        self.shot = 0
