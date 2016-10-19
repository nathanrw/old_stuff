import os

import pygame
from pygame.locals import *

import weakref

from vector2D import Vector2D
from fov import makePrettyFieldOfView

import config

import math

try:
    import psyco
    psyco.full()
except:
    print "Unable to import psyco."

image_path = os.path.join("data", "images")
sound_path = os.path.join("data", "sounds")

def getImg(name):
    return pygame.image.load(os.path.join(image_path, name))

#******************************************************************************
# A spritesheet.
#******************************************************************************
class SpriteSheet():
    
    def __init__(self, sheet, tilesize):
        self.sheet = sheet
        self.tilesize = tilesize
        self.cache = {}
        
        self.spritesPerRow = self.sheet.get_width()/self.tilesize
        
    def __getitem__(self, index):
        
        if index in self.cache.keys():
            return self.cache[index]
        
        y = (index / self.spritesPerRow) * (self.tilesize+1)
        x = (index % self.spritesPerRow) * (self.tilesize+1)
        
        rect = Rect(x, y, self.tilesize, self.tilesize)
        img = self.sheet.subsurface(rect).copy().convert()
        img.set_colorkey(img.get_at((0,0)))
        
        self.cache[index] = img
        
        return img

#******************************************************************************
# Lazy resource loading - nicked out of the cookbook.
#******************************************************************************
class LazyResourceController():
    
    def __init__(self, loading_function):
        
        self.cache = weakref.WeakValueDictionary()
        self.names = {}
        self.loading_function = loading_function
    
    def __setattr(self, name, value):
        self.names[name] = value
    
    def __getattr__(self, name):
        
        if name in self.cache.keys():
            obj = self.loading_function(self.cache[name])
        else:
            obj = self.loading_function(self.names[name])
            self.cache[name] = obj
        return obj

#******************************************************************************
# Images are got through this.
#******************************************************************************
class LazyImageController(LazyResourceController):
    
    def __init__(self):
        
        def loading_function(name, alpha=0):
            img = pygame.image.load(os.path.join(image_path, name))
            if alpha == 2:
                img = img.convert_alpha()
            elif alpha == 1:
                img = img.convert()
                colorkey = img.get_at((0,0))
                img.set_colorkey(colorkey)
            else:
                img = img.convert()
            return img
        f = lambda filename: loading_function(filename, 1)
        LazyResourceController.__init__(self, f)

#******************************************************************************
# Sounds are got through this.
#******************************************************************************
class LazySoundController(LazyResourceController):
    
    def __init__(self):
        
        def loading_function(name, volume=1):
            snd = pygame.mixer.Sound(os.path.join(sound_path, name))
            return snd
        LazyResourceController.__init__(self, loading_function)

#******************************************************************************
# You can only see in front of you.
#******************************************************************************
class FieldOfView():
    
    def __init__(self, dest_rect, fov, rotation):
        
        self.dest_rect = dest_rect
        self.fov = fov
        self.rotation = rotation
        
        self.redraw_image()
        self.rotate_image()
    
    def redraw_image(self):
        self.image = makePrettyFieldOfView(self.dest_rect, self.fov, 0, 20)
    
    def rotate_image(self):
        angle = math.degrees(self.rotation)
        self.rotated_image = pygame.transform.rotate(self.image, angle)
    
    def set_rotation(self, angle):
        self.rotation = angle
        if self.rotation > math.pi*2:
            self.rotation -= math.pi*2
        elif self.rotation < 0:
            self.rotation += math.pi*2
        self.rotate_image()
    
    def set_fov(self):
        self.fov = fov
        self.redraw_image()
        self.rotate_image()
    
    def rotate(self, angle):
        self.set_rotation(self.rotation + angle)
    
    def draw(self, surface, centre=None):
        rect = self.rotated_image.get_rect()
        if centre is not None:
            rect.center = centre
        else:
            rect.center = surface.get_rect().center
        surface.blit(self.rotated_image, rect)

#******************************************************************************
# Basic sprite.
#******************************************************************************
class GameSprite(pygame.sprite.Sprite):
    
    anims = None
    sounds = None
    s = 5
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((40,40))
        self.rect = self.image.get_rect()
        
        self.animspeed = self.s
        self.animcounter = 0.0
        self.frametime = 1.0/config.framerate*self.animspeed
        
        self.position = Vector2D(0,0)
    
    def setAnimspeed(self, speed):
        self.animspeed = speed
        self.frametime = 1.0/config.framerate*self.animspeed
    
    def update(self):
        self.animcounter += self.frametime
        if self.animcounter >= len(self.current_anim):
            self.animcounter = 0.0
        self.image = self.current_anim[int(self.animcounter)]
        self.dirty = True

#******************************************************************************
# Units
#******************************************************************************
class UnitSprite(GameSprite):
    
    def __init__(self):
        GameSprite.__init__(self)
        
        self.direction = "up"
        self.change_state("move")
        self.speed = 1
    
    def update(self):
        GameSprite.update(self)
    
    def walk(self):
        self.move(self.direction)
    
    def move(self, direction):
        
        if direction != self.direction: self.change_direction(direction)
        
        if self.direction == "left":
            self.position.x = self.position.x - self.speed
        elif self.direction == "right":
            self.position.x = self.position.x + self.speed
        elif self.direction == "up":
            self.position.y = self.position.y - self.speed
        elif self.direction == "down":
            self.position.y = self.position.y + self.speed
        
        self.dirty = True
    
    def change_state(self, state):
        
        self.state = state
        self.current_anim = self.anims[self.state][self.direction]
        self.rect.size = self.current_anim[0].get_rect().size
        self.animcounter = 0
    
    def change_direction(self, direction):
        
        self.direction = direction
        self.current_anim = self.anims[self.state][self.direction]
        self.animcounter = 0

#******************************************************************************
# Gravestones and stuff
#******************************************************************************
class ScenerySprite(GameSprite):
    def __init__(self):
        GameSprite.__init__(self)

class TorchLight(GameSprite):
    anims = {"on":None, "off":[pygame.Surface((10,10), SRCALPHA)]}
    
    def __init__(self):
        GameSprite.__init__(self)
        self.baseangle = math.pi/4
        self.angle = self.baseangle
        self.change_state("off")
        self.jiggle = 50
    
    def change_state(self, state):
        self.state = state
        self.current_anim = self.anims[self.state]
        self.animcounter = 0
    
    def setAngle(self, angle):
        self.baseangle = angle + math.pi/4
        self.angle = self.baseangle
    
    def update(self):
        GameSprite.update(self)
        self.angle = self.baseangle + math.sin(self.animcounter)/self.jiggle
        self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))
        self.rect = self.image.get_rect()
        self.rect.center = self.centre
    
    def switch(self):
        if self.state == "on": self.change_state("off")
        elif self.state == "off": self.change_state("on")

#******************************************************************************
# You.
#******************************************************************************
class Player(UnitSprite):
    def __init__(self):
        UnitSprite.__init__(self)
    def move(self, direction):
        if direction == "up": self.world.move(0, self.speed)
        if direction == "down": self.world.move(0, -self.speed)
        if direction == "left": self.world.move(self.speed, 0)
        if direction == "right": self.world.move(-self.speed, 0)

#******************************************************************************
# BRAAAAINS
#******************************************************************************
class Baddie(UnitSprite):
    pass

#******************************************************************************
# Everything that needs moving with the player.
#******************************************************************************
class World():
    def __init__(self, *groups):
        self.groups = groups
    def move(self, x, y):
        for group in self.groups:
            for sprite in group:
                sprite.rect.x += x
                sprite.rect.y += y

#******************************************************************************
# Basic game state.
#******************************************************************************
class GameState():
    
    def handleEvents(self): pass
    def update(self): pass
    def draw(self): pass
    def mainLoop(self):
        while 1:
            if self.handleEvents() == 0:
                pygame.quit()
                return
            self.update()
            self.draw()

#******************************************************************************
# Main menu.
#******************************************************************************
class Menu(GameState):
    pass

#******************************************************************************
# The game.
#******************************************************************************
class Main(GameState):
    
    def __init__(self):
        
        ## Initialise parts of pygame.
        
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800,600))
        self.background = pygame.Surface((self.screen.get_rect().size))
        
        ## Objects to keep track of data and load it when needed.
        
        self.images = LazyImageController()
        self.sounds = LazySoundController()
        self.spriteSheet = SpriteSheet(getImg("spritesheet.png"), 64)
        
        ## Load sounds + images.
        
        self.images.torchlight = "torch.png"
        
        ## Assign anims and sounds to sprites.
        
        Player.anims = {
                        "idle": {
                                 "up":[
                                       self.spriteSheet[0]
                                      ],
                                 "right": [
                                          self.spriteSheet[3]
                                         ],
                                 "down": [
                                          self.spriteSheet[6]
                                         ],
                                 "left": [
                                           self.spriteSheet[9]
                                          ]
                                },
                        "move": {
                                 "up":[
                                       self.spriteSheet[0],
                                       self.spriteSheet[1],
                                       self.spriteSheet[2]
                                      ],
                                 "right": [
                                          self.spriteSheet[3],
                                          self.spriteSheet[4],
                                          self.spriteSheet[5]
                                         ],
                                 "down": [
                                          self.spriteSheet[6],
                                          self.spriteSheet[7],
                                          self.spriteSheet[8]
                                         ],
                                 "left": [
                                           self.spriteSheet[9],
                                           self.spriteSheet[10],
                                           self.spriteSheet[11]
                                          ]
                                },
                       }
        
        # Temporary baddie anims.
        a = pygame.image.load("data/images/none.png").convert_alpha()
        b = pygame.transform.flip(a, 1, 0)
        c = pygame.transform.flip(a, 0, 1)
        d = pygame.transform.flip(a, 1, 1)
        
        Baddie.anims = {
                        "idle": {
                               "up":[a],
                               "down":[a],
                               "left":[a],
                               "right":[a]
                               },
                        "move":{
                               "up":[b],
                               "down":[b],
                               "left":[b],
                               "right":[b]
                               },
                        "hit": {
                               "up":[c],
                               "down":[c],
                               "left":[c],
                               "right":[c]
                               },
                        "stop":{
                               "up":[c],
                               "down":[c],
                               "left":[c],
                               "right":[c]
                               },
                        "die": {
                               "up":[d],
                               "down":[d],
                               "left":[d],
                               "right":[d]
                               }
                       }
        
        TorchLight.anims["on"] = [pygame.image.load("data/images/torch.png").convert_alpha()]
        
        ## Object draws the field of view.
        
        self.fov = FieldOfView(self.screen.get_rect(), math.pi-math.pi/9,0)
        
        ## Time.
        
        self.clock = pygame.time.Clock()
        
        ## Keys being held down.
        
        self.FORWARD = 0
        self.BACKWARD = 0
        self.LEFT = 0
        self.RIGHT = 0
        self.RUN = 0
        
        ## Groups for game objects
        
        self.group_all = pygame.sprite.RenderUpdates()
        self.group_player = pygame.sprite.Group()
        self.group_baddies = pygame.sprite.Group()
        self.group_terrain = pygame.sprite.Group()
        
        Player.world = World(self.group_baddies, self.group_terrain)
        
        ## Setup groups
        
        #Player.groups = [self.group_all, self.group_player]
        #Baddie.groups = [self.group_all, self.group_baddies]
        
        ## Make game objects
        
        self.player = Player()
        self.player.add(self.group_all)
        self.player.rect.center = (config.screenres[0]/2, config.screenres[1]/2)
        
        b = Baddie()
        b.add(self.group_all, self.group_baddies)
        
        TorchLight.centre = self.screen.get_rect().center
        self.torchlight = TorchLight()
        self.torchlight.add(self.group_all)
    
    def checkBaddieInSector(self, baddie, centre, r, A, B):
        if abs((baddie.getPos() - centre).magnitude()) > r: return 0
        bearing = baddie.getPos().angleBetween(Vector2D(0,1))
        if not (A-B/2 < bearing < A+B/2): return 0
        return 1
    
    def handleEvents(self):
        
        for e in pygame.event.get():
            
            if e.type == QUIT:
                return 0
            
            elif e.type == KEYDOWN:
                
                if e.key == K_ESCAPE:
                    return 0
                
                elif e.key == K_w: self.FORWARD = 1
                elif e.key == K_s: self.BACKWARD = 1
                elif e.key == K_a: self.LEFT = 1
                elif e.key == K_d: self.RIGHT = 1
                elif e.key == K_f: self.torchlight.switch()
                elif e.key == K_LSHIFT: self.RUN = 1
            
            elif e.type == KEYUP:
                
                if e.key == K_ESCAPE:
                    return 0
                
                elif e.key == K_w: self.FORWARD = 0
                elif e.key == K_s: self.BACKWARD = 0
                elif e.key == K_a: self.LEFT = 0
                elif e.key == K_d: self.RIGHT = 0
                elif e.key == K_LSHIFT: self.RUN = 0
            
            elif e.type == MOUSEBUTTONDOWN:
                pass
            
            elif e.type == MOUSEBUTTONUP:
                pass
            
            elif e.type == MOUSEMOTION:
                pass
        
        return 1
    
    def update(self):
        
        if self.FORWARD:
            rot = math.radians(0)
            self.fov.set_rotation(rot)
            if self.player.direction != "up":
                self.player.change_direction("up")
                self.torchlight.setAngle(rot)
        if self.BACKWARD:
            rot = math.radians(180)
            self.fov.set_rotation(rot)
            if self.player.direction != "down":
                self.player.change_direction("down")
                self.torchlight.setAngle(rot)
        if self.LEFT:
            rot = math.radians(90)
            self.fov.set_rotation(rot)
            if self.player.direction != "left":
                self.player.change_direction("left")
                self.torchlight.setAngle(rot)
        if self.RIGHT:
            rot = math.radians(270)
            self.fov.set_rotation(rot)
            if self.player.direction != "right":
                self.player.change_direction("right")
                self.torchlight.setAngle(rot)
        
        if not (self.FORWARD | self.BACKWARD | self.LEFT | self.RIGHT):
            if self.player.state == "move":
                self.player.change_state("idle")
                self.torchlight.jiggle = 100
        else:
            self.player.walk()
            self.torchlight.jiggle = 25
            if self.player.state == "idle":
                self.player.change_state("move")    
            if self.RUN:
                self.player.speed = 12
                self.torchlight.jiggle = 10
            else:
                self.player.speed = 6
        
        self.clock.tick(config.framerate)
        
        self.group_all.update()
        for b in self.group_baddies:
            c = Vector2D(self.screen.get_rect().center)
            
            r1 = self.torchlight.getRadius()
            A1 = self.torchlight.getRotation()
            B1 = self.torchlight.getArc()
            
            r2 = math.sqrt((self.screen.get_width()/2)**2+(self.screen.get_height()/2)**2)
            A2 = self.fov.getRotation()
            B2 = math.pi*2 - self.fov.getFOV()
            
            if self.checkBaddieInSector(b,c,A1,B1):
                if b.state != "die" and self.torchlight.state =="on":
                    b.change_state("die")
            
            if self.checkBaddieInSector(b,c,A2,B2):
                if b.state != "stop" and b.state != "die":
                    b.change_state("stop")
    
    def draw(self):
        
        #self.group_all.clear(self.screen, self.background)
        self.screen.fill((50,50,50))
        self.group_all.draw(self.screen)
        
        d = 10
        
        rect = self.screen.get_rect()
        x, y = rect.center[0], rect.center[1]
        
        if self.player.direction == "up":
            y += d
        elif self.player.direction == "down":
            y -= (d + 10)
        elif self.player.direction == "left":
            x += d
        else:
            x -= d
            
        centre = (x, y)
            
        self.fov.draw(self.screen, centre)
        
        
        pygame.display.update()

#******************************************************************************
# Closing screen.
#******************************************************************************
class End(GameState):
    pass

#******************************************************************************

class Game():
    
    def __init__(self):
        pass
    
    def mainLoop(self):
        Main().mainLoop()

#******************************************************************************

def main():
    Game().mainLoop()

if __name__ == '__main__':
    main()