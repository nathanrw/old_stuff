# tetris

import pygame
from pygame.locals import *

SHAPE_S = [[0, 1, 1],
           [1, 1, 0]]
        
SHAPE_Z = [[1, 1, 0],
           [0, 1, 1]]
        
SHAPE_LINE = [[1],
              [1],
              [1],
              [1]]
            
SHAPE_SQUARE = [[1, 1],
                [1, 1]]
                
SHAPE_L = [[1, 0],
           [1, 0],
           [1, 1]]
        
SHAPE_J = [[0, 1],
           [0, 1],
           [1, 1]]

COLOURS = {
           SHAPE_S : (0, 0, 0),
           SHAPE_Z : (0, 0, 0),
           SHAPE_LINE : (0, 0, 0),
           SHAPE_SQUARE : (0, 0, 0),
           SHAPE_L : (0, 0, 0),
           SHAPE_J : (0, 0, 0)
          }

SHAPES = (SHAPE_S, SHAPE_Z, SHAPE_LINE, SHAPE_SQUARE, SHAPE_L, SHAPE_J)

class Game:
    
    def __init__(self):
        
        self.tilesize = 16
        self.display_size = (800, 600)
        
        ####
        
        pygame.init()
        
        self.display = pygame.display.set_mode(self.display_size)
        self.background = pygame.Surface(self.display.size)
        
        self.gridsize = (self.display_size[0]//self.tilesize,
                         self.displaysize[1]//self.tilesize)
        
        self.grid = []
        
        for y in xrange(self.gridsize[1]):
            
            self.grid.append([])
            
            for x in xrange(self.gridsize[0]):
                
                self.grid[y].append(0)
        
        shape = random.choice(SHAPES)
        
        self.block = self.get_block()
        
        self.running = 1
    
    def handle_events(self):
        
        for e in pygame.event.get():
            
            if e.type == QUIT:
                
                self.running = 0
            
            elif e.type == KEYDOWN:
                
                if e.key == K_ESCAPE:
                    
                    self.running = 0
                
                elif e.key == K_LEFT:
                    
                    self.block.move_horizontal(-1)
                
                elif e.key == K_RIGHT:
                    
                    self.block.move_horizontal(1)
                
                elif e.key == K_UP:
                    
                    self.block.rotate(1)
                
                elif e.key == K_DOWN:
                    
                    self.block.move_vertical(1)
                    
                elif e.key == K_SPACE:
                    
                    self.block.drop()
    
    def clear_lines(self):
        
        for line in self.grid:
            
            if not 0 in line:
                
                self.grid.remove(line)
                self.grid.insert(0, [])
                
                for x in xrange(self.gridsize[0]):
                
                    self.grid[0].append(0)
    
    def update(self):
        
        self.block.update()
        
        if self.block.dead:
            
            self.block.draw(self.background)
            self.block.add_to_grid(self.grid)
            self.block = self.get_block()
            
            self.clear_lines()
    
    def get_block(self):
        
        return Block(shape, self.grid, random.randrange(0, len(self.grid)-len(shape[0])), 0, self.speed, self.tilesize)
    
    def draw(self):
        
        self.display.blit(self.background, (0, 0))
        
        self.block.draw_shadow(self.display)
        self.block.draw(self.display)
        
        pygame.display.update()
    
    def mainLoop(self):
        
        while self.running:
            
            self.handle_events()
            self.update()
            self.draw()

class Block:
    
    def __init__(self, shape, grid, x, y, speed, size):
        
        self.shape = shape # base shape
        self.current_shape = shape # shape rotated
        
        self.x = x
        self.y = y
        
        self.speed = speed
        
        self.arena = grid
        self.arena_x = len(self.arena[0])
        self.arena_y = len(self.arena)
        
        self.rotation = 0 # 0,1,2,3 -> 0, 90, 180, 270
        
        self.size = size
        
        self.colour = self.colour()
        
        self.contactcounter = 0 # how long the block has been at rest on top of something.
        self.contactlimit = 200
        
        self.possible_shapes = {}
        
        for n in xrange(4):
            
            self.possible_shapes[n] = self.__rotate(n)
        
        if self.collide_detect(self.x, self.y, self.current_shape):
            
            print "Block spawned in another one :("
        
        self.dead = 0
    
    def colour(self):
        
        return COLOURS[self.shape]
    
    def __rotate(self, rotations):
        
        shape = self.shape
        
        for n in xrange(rotations):
            
            width = len(shape)
            height = len(shape[0])
            
            new_shape = []
            
            for y in xrange(height):
                
                new_shape.append([])
                
                for x in xrange(width):
                    
                    new_shape[y].append(shape[x][height-1-y])
            
            shape = new_shape
        
        return shape
    
    def rotate(self, left_or_right):
        
        self.contactcounter = 0
        
        if left_or_right:
            
            self.rotation -= 1
            if self.rotation == -1:
                self.rotation = 3
        
        else:
            
            self.rotation += 1
            if self.rotation == 4:
                self.rotation = 0
        
        self.current_shape = self.possible_shapes[self.rotation]
        
        self.resolve_overlap()
    
    def resolve_overlap(self):
        while self.detect_collision(self.x, self.y, self.current_shape):
            self.y -= 1
        
    def move(self):
        
        if not self.detect_collision(self.x, self.y + self.speed, self.current_shape):
            
            self.y += 1
        
        else:
            
            self.contactcounter += 1
            
            if self.contactcounter > self.contactlimit:
                
                self.dead = 1
    
    def move_horizontal(self, dx):
        
        if not self.detect_collision(self.x+dx, self.y, self.current_shape):
            
            self.x += dx

    def move_vertical(self, dy):
        
        if not self.detect_collision(self.x, self.y+dy, self.current_shape):
            
            self.y += dy
    
    def drop(self):
        
        dy = 0
        
        while not self.detect_collision(self.x, self.y+dy, self.current_shape):
            
            dy += 1
        
        self.y += dy
        self.dead = 1
    
    def detect_collision(self, Px, Py, shape):
        
        for Sx in xrange(shape[0]):
            
            for Sy in xrange(shape):
                
                Wx = Px + Sx
                Wy = Py + Sy
                
                try:
                    
                    if self.grid[Wy][Wx] == 1:
                    
                        return 1
                
                except IndexError:
                    
                    return 1
        
        return 0
    
    def add_to_grid(self, grid):
        
        for x in xrange(len(self.current_shape[0])):
            
            for y in xrange(len(self.current_shape)):
                
                grid[y+self.y][x+self.x] = 1
    
    def update(self):
        
        if self.movecounter > self.movelimit:
            self.move()
    
    # Improve the stuff below at some point
    
    def draw_block(self, x, y, colour, surf):
        
        x = (x + self.x) * self.size
        y = (y + self.y) * self.size
        
        rect = Rect(x, y, self.size, self.size)
        rect = rect.inflate((-2. -2))
        
        pygame.draw.rect(surf, colour, rect)
    
    def draw(self, surf):
        
        for x in xrange(len(self.current_shape[0])):
            
            for y in xrange(len(self.current_shape)):
                
                self.draw_block(x, y, self.colour, surf)
    
    def draw_shadow(self, surf):
        
        dy = 0
        
        while not self.detect_collision(self.x, self.y+dy, self.current_shape):
            
            dy += 1
            
        for x in xrange(len(self.current_shape[0])):
            
            for y in xrange(len(self.current_shape)):
                
                self.draw_block(x, y+dy, (100,100,100), surf)