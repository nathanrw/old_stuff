from vec2d import vec2d
import pygame
from pygame.locals import *
import math
from math import sin, cos, hypot, atan2, degrees, ceil

def tileImageAlongLine(surf, img, start, end):
    
    # Displacement between the two points and its magnitude.
    displacement = vec2d(start[0]-end[0], start[1]-end[1])
    length = hypot(displacement.x, displacement.y)
    
    # No need to draw anything.
    if length <= 0:
        return
    
    # Save typing it out a lot.
    w = img.get_width()
    h = img.get_height()
    
    # Tile the image along a surface as long as the line.
    
    tiled = pygame.Surface((length, h), SRCALPHA)
    numtiles = int(ceil(length / w))
    
    for x in range(0, numtiles):
        tiled.blit(img, (x*w, 0))
    
    # Get the required angle and rotate the tiled image accordingly.
    angle = atan2(-displacement[1],displacement[0])
    rotated = pygame.transform.rotozoom(tiled, degrees(angle), 1)
    
    # Position the image on the surface it is being drawn to.
    rect = rotated.get_rect()
    rect.center = vec2d(start) - displacement*0.5
    
    # Draw the finished surface.
    surf.blit(rotated, rect)

class LineTrail():
    def __init__(self, img, speed, rotation, length, time, get_pos):
        
        self.speed = speed
        self.rotation = rotation
        self.length = length
        self.time = time
        self.get_pos = get_pos
        self.pos = vec2d(self.get_pos())
        self.points = []
        self.img = img
        self.lastremoved=0
    
    def update(self):
        
        self.pos = vec2d(self.get_pos())
        
        if len(self.points) >= self.length and pygame.time.get_ticks()-self.lastremoved>self.time:
            self.points.remove(self.points[0])
            self.lastremoved = pygame.time.get_ticks()
        
        if len(self.points) < self.length:
            vel = vec2d(self.speed * cos(self.rotation),
                        self.speed * sin(self.rotation))
            self.points.append([vec2d(self.pos),vel])
        
        for point in self.points:
            point[0] += point[1]
    
    def draw(self, surface):
        index = 0
        points = []
        for point in self.points:
            points.append(point[0])
        end = len(points)-1
        while index < end:
            tileImageAlongLine(surface, self.img, points[index],points[index+1])
            index += 1

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((800,600))
    
    img = pygame.image.load("01laser.png").convert_alpha()
    trail = LineTrail(img,5,0,4,50,pygame.mouse.get_pos)
    
    clock = pygame.time.Clock()
    
    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.display.quit()
                return
            if e.type == MOUSEMOTION:
                trail.rotation = math.atan2(e.rel[0],-e.rel[1])+math.pi/2
        trail.update()
        screen.fill((0,0,0))
        trail.draw(screen)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()