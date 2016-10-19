#=====================================================================
# Dodgy arcade game thing
#
#
#=====================================================================

import os, sys
import math
import random
import pygame
import threading
import winsound
from pygame.locals import *

class PlaySound(threading.Thread):
    
    def run(self):
        #winsound.Beep(random.random()*1000+150,50 )
        winsound.MessageBeep(-1)

# Thing

class Thing():
    def __init__(self, Px, Py, Vx, Vy, points, colour, *groups):
        self.groups = groups
        for group in groups:
            group.append(self)
        self.Px = Px
        self.Py = Py
        self.Vx = Vx
        self.Vy = Vy
        self.points = points
        self.colour = colour
    def setPosition(self, x, y):
        self.Px = x
        self.Py = y
    def getPosition(self):
        return self.Px, self.Py
    def setVelocity(self, x, y):
        self.Vx = x
        self.Vy = y
    def getVelocity(self):
        return self.Vx, self.Vy
    def getPoints(self):
        points = []
        for point in self.points:
            points.append((point[0]+self.Px, point[1]+self.Py))
        return points
    def update(self):
        self.Px += self.Vx
        self.Py += self.Vy
    def draw(self, surface):
        pygame.draw.lines(surface, self.colour, 1, self.getPoints())
        if self.Px < 0:
            self.kill()
        elif self.Px > 800:
            self.kill()
        if self.Py < 0:
            self.kill()
        elif self.Py > 600:
            self.kill()
    def kill(self):
        for group in self.groups:
            if group.__contains__(self):
                group.remove(self)
    
    def move(self, x, y):
        self.Px += x
        self.Py += y
    def detectCollide(self, Px, Py):
        dx = Px - self.Px
        dy = Py - self.Py
        r = math.hypot(dx, dy)
        if r < self.s:
            self.getHit()
            return 1
        return 0

# Player

class Player(Thing):
    def __init__(self, Px, Py, Vx, Vy, points, colour, *groups):
        Thing.__init__(self, Px, Py, Vx, Vy, points, colour, *groups)

# Shot

class Shot(Thing):
    def __init__(self, Px, Py, *groups):
        
        Vx = random.random()*random.choice((-1,1))
        Vy = -6
        
        points = [(0,-10),(5,10),(-5,10)]
        colour = (0,255,0)
        
        Thing.__init__(self, Px, Py, Vx, Vy, points, colour, *groups)

# EShot

class EShot(Thing):
    def __init__(self, Px, Py, *groups):
        Vx = random.random()*random.choice((-1,1))
        Vy = -6
        
        points = [(0,-10),(5,10),(-5,10)]
        colour = (0,255,0)
        
        Thing.__init__(self, Px, Py, Vx, Vy, points, colour, *groups) 

# Enemy

class Enemy(Thing):
    def __init__(self, *groups):
        
        Px = random.random()*800
        Py = random.random()*200
        
        Vx = 0
        Vy = 0
        
        s = 20
        self.s = s
        points = [(0,s),(-s,0),(-s/2,-s),(s/2,-s),(s,0)]
        colour = [255,0,0]
        
        Thing.__init__(self, Px, Py, Vx, Vy, points, colour, *groups)
        
        self.ticker = 0
        self.health = 50+ random.randrange(0,25)
        self.flashing = 0
        self.numflashes = 0
        self.maxflashes = 6
    
    def getHit(self):
        self.health -= 1
        self.flashing = 1
        if self.health == 0:
            self.kill()
    
    def handleFlashing(self):
        if self.flashing:
            self.ticker += 1
            if self.ticker > 6:
                self.ticker = 0
                if self.colour == (255,0,0):
                    self.colour = (255,255,0)
                else:
                    self.colour = (255,0,0)
                self.numflashes += 1
                if self.numflashes > self.maxflashes:
                    self.colour = (255,0,0)
                    self.flashing = 0
                    self.ticker = 0
                    self.numflashes = 0
                    
    def ai(self):
        
        if math.hypot(self.Vx,self.Vy) < 6:
            self.Vx += random.random()*random.choice((1,-1))
            self.Vy += random.random()*random.choice((1,-1))
        
        if self.Px + self.Vx < 0:
            self.Vx = 1
        elif self.Px + self.Vx > 800:
            self.Vx = -1
        if self.Py + self.Vy < 0:
            self.Vy = 1
        elif self.Py + self.Vy > 300:
            self.Vy = -1
                    
    def update(self):
        Thing.update(self)
        self.handleFlashing()
        self.ai()

# Game

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,600))
        self.all = []
        self.shots = []
        self.enemies = []
        playerpoints = [(0,-50),(25,50),(-25,50)]
        self.player = Player(400, 500, 0, 0, playerpoints, (0,0,255), self.all)
        self.clock = pygame.time.Clock()
        
        self.shooting = 0
        self.xMove = 0
        self.yMove = 0
        self.playerspeed = 6
        
    def run(self):
        while 1:
            if self.getInput() == 0:
                break
            self.update()
            self.draw()
            
    def getInput(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return 0
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    return 0
                
                if e.key == K_UP:
                    self.yMove = -1
                elif e.key == K_DOWN:
                    self.yMove = 1
                elif e.key == K_LEFT:
                    self.xMove = -1
                elif e.key == K_RIGHT:
                    self.xMove = 1
                
                elif e.key == K_z:
                    self.shooting = 1
                    
            elif e.type == KEYUP:
                
                if e.key == K_UP:
                    self.yMove = 0
                elif e.key == K_DOWN:
                    self.yMove = 0
                elif e.key == K_LEFT:
                    self.xMove = 0
                elif e.key == K_RIGHT:
                    self.xMove = 0
                    
                elif e.key == K_z:
                    self.shooting = 0
                    
        return 1
    
    def addEnemies(self):
        if len(self.enemies) < 5:
            if random.random() > 0.5:
                Enemy(self.enemies, self.all)
    
    def update(self):
        
        self.addEnemies()
        
        if self.shooting:
            Shot(self.player.Px, self.player.Py,self.shots, self.all)
        
        self.player.move(self.xMove*self.playerspeed, self.yMove*self.playerspeed)
        
        for item in self.all:
            item.update()
        
        for shot in self.shots:
            for enemy in self.enemies:
                if enemy.detectCollide(shot.Px, shot.Py):
                    shot.kill()
        
        self.clock.tick(60)
        
    def draw(self):
        self.screen.fill((0,0,0))
        for item in self.all:
            item.draw(self.screen)
        pygame.display.update()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    try:
        main()
    except:
        sys.excepthook(*sys.exc_info())
        wait = raw_input("Any key lol")