#******************************************************************************
#
# Tetris Clone
#
#******************************************************************************

import pygame
from pygame.locals import *
import random

BLOCKWIDTH = 16
BLOCKHEIGHT = 16

ARENAHEIGHT = 25
ARENAWIDTH = 10

BLOCKS = None

def drawBlock(x, y, surface, val):
    if not val: return
    x = x*BLOCKWIDTH
    y = y*BLOCKHEIGHT
    
    surface.blit(BLOCKS[val], (x, y))
    
def makeArena():

    arena = []
    
    for y in range(0, ARENAHEIGHT):
        row = []
        for x in range(0, ARENAWIDTH):
            row.append(0)
        arena.append(row)
    
    return arena

class Tetromino():
    arena = None
    
    def __init__(self, x):
        self.contact_time = 1
        self.contact_timer = 0
        
        self.x = x
        
        diff = self.x + len(self.shape[0]) - len(self.arena[0])
        if diff > 0: self.x -= diff
        
        self.y = 0
    
    def paint(self):
        for y, row in enumerate(self.shape):
            for x, val in enumerate(row):
                if val == 0: continue
                self.arena[self.y+y][self.x+x] = val
    
    def unpaint(self):
        for y, row in enumerate(self.shape):
            for x, val in enumerate(row):
                if val == 0: continue
                self.arena[self.y+y][self.x+x] = 0
    
    def move(self, x_move, y_move):
        if x_move:
            
            x_collide = 0
            for y in range(0, len(self.shape)):
                
                # Left collisions:
                
                # At edge of field, no more movement allowed.
                if self.x == 0 and x_move < 0:
                    x_collide = 1
                    break
                
                if self.x != 0 and x_move < 0:
                    
                    for x in range(0, len(self.shape[0])):
                        
                        if self.shape[y][x] != 0:
                            left = x
                            break
                        
                    if self.arena[y + self.y][left + self.x - 1] != 0:
                        x_collide = 1
                
                # Right collisions
                
                # At edge of field, no more movement allowed.
                if self.x == len(self.arena[0])-1 and x_move > 0:
                    x_collide = 1
                    break
                
                if self.x < len(self.arena[0])-1 and x_move > 0:
                    
                    r = range(0, len(self.shape[0]))
                    r.reverse()
                    for x in r:
                        
                        if self.shape[y][x] != 0:
                            right = x
                            break
                        
                    if self.arena[y + self.y][right + self.x + 1] != 0:
                        x_collide = 1
                
                if x_collide == 1: break
            
            if not x_collide:
                self.x += x_move
        
        if y_move:
            y_collide = 0
            
            for x in range(0, len(self.shape[0])):
                
                if self.y+len(self.shape) == len(self.arena):
                    y_collide = 1
                    break
                
                r = range(0, len(self.shape))
                r.reverse()
                
                for y in r :
                    if self.shape[y][x] != 0:
                        bottom = y
                        break
                
                if self.arena[self.y + bottom + 1][self.x + x] != 0:
                    y_collide = 1
                    break
            
            if not y_collide:
                self.contact_timer = 0
                self.y += y_move
            else:
                self.contact_timer += 1
    
    def inContact(self):
        if self.contact_timer > self.contact_time:
            return 1
    
    def place(self):
        pass
    
    def rotate(self):
        newshape = []
        for x in range(0, len(self.shape[0])):
            newrow = []
            r = range(0, len(self.shape))
            r.reverse()
            for y in r:
                newrow.append(self.shape[y][x])
            newshape.append(newrow)
        self.shape = newshape

class O(Tetromino):
    def __init__(self, x):
        self.shape = [[1,1],[1,1]]
        Tetromino.__init__(self, x)

class I(Tetromino):
    def __init__(self, x):
        self.shape = [[2],[2],[2],[2]]
        Tetromino.__init__(self, x)
        
class S(Tetromino):
    def __init__(self, x):
        self.shape = [
                      [0,3,3],
                      [3,3,0]
                     ]
        Tetromino.__init__(self, x)    

class T(Tetromino):
    def __init__(self, x):
        self.shape = [
                      [0,4,0],
                      [4,4,4]
                     ]
        Tetromino.__init__(self, x)

class Z(Tetromino):
    def __init__(self, x):
        self.shape = [
                      [5,5,0],
                      [0,5,5]
                     ]
        Tetromino.__init__(self, x)

class J(Tetromino):
    def __init__(self, x):
        self.shape = [
                      [6,0,0],
                      [6,6,6]
                     ]
        Tetromino.__init__(self, x)

class L(Tetromino):
    def __init__(self, x):
        self.shape = [
                      [0,0,7],
                      [7,7,7]
                     ]
        Tetromino.__init__(self, x)

class TetrominoMaker():
    
    def __init__(self):
        self.types = [O, I, S, T, Z, J, L]
    
    def pick(self):
        return random.choice(self.types)

class Game():
    
    def __init__(self):
        
        pygame.init()
        
        self.arena = makeArena()
        
        Tetromino.arena = self.arena
        
        self.tetrominoMaker = TetrominoMaker()
        
        self.placeTetromino()
        
        screenx = BLOCKWIDTH*ARENAWIDTH
        screeny = BLOCKHEIGHT*ARENAHEIGHT
        self.screen = pygame.display.set_mode((screenx,screeny))
        
        self.clock = pygame.time.Clock()
        
        global BLOCKS
        
        BLOCKS = {
                  1:pygame.image.load("block_red.png").convert_alpha(),
                  2:pygame.image.load("block_blue.png").convert_alpha(),
                  3:pygame.image.load("block_lightblue.png").convert_alpha(),
                  4:pygame.image.load("block_yellow.png").convert_alpha(),
                  5:pygame.image.load("block_pink.png").convert_alpha(),
                  6:pygame.image.load("block_brown.png").convert_alpha(),
                  7:pygame.image.load("block_green.png").convert_alpha()
                 }
        
        self.blocktime = 20
        self.blocktimer = 0
        
        self.LEFT = 0
        self.RIGHT = 0
        self.DOWN = 0
        self.UP = 0
    
    def placeTetromino(self):
        tet = self.tetrominoMaker.pick()
        self.current_tetromino = tet(random.randrange(0,10))
    
    def handleEvents(self):
        for e in pygame.event.get():
            
            if e.type == QUIT:
                return 1
            
            elif e.type == KEYDOWN:
                
                if e.key == K_ESCAPE:
                    return 1
                elif e.key == K_LEFT:
                    self.LEFT = 1
                elif e.key == K_RIGHT:
                    self.RIGHT = 1
                elif e.key == K_DOWN:
                    self.DOWN = 1
                elif e.key == K_UP:
                    self.UP = 1
            
            elif e.type == KEYUP:
                
                if e.key == K_LEFT:
                    self.LEFT = 0
                elif e.key == K_RIGHT:
                    self.RIGHT = 0
                elif e.key == K_DOWN:
                    self.DOWN = 0
                elif e.key == K_UP:
                    self.UP = 0
        
        return 0
    
    def update(self):
        
        self.current_tetromino.unpaint()
        
        self.blocktimer += 1
        if self.blocktimer == self.blocktime:
            self.current_tetromino.move(0, 1)
            self.blocktimer = 0
            
        if self.LEFT:
            self.current_tetromino.move(-1,0)
            self.LEFT = 0
        elif self.RIGHT:
            self.current_tetromino.move(1, 0)
            self.RIGHT = 0
        elif self.DOWN:
            self.current_tetromino.move(0, 1)
        elif self.UP:
            self.current_tetromino.rotate()
            self.UP = 0
            
        for row in self.arena:
            isfull = 1
            for item in row:
                if item == 0:
                    isfull = 0
            if isfull:
                self.arena.remove(row)
                self.arena.reverse()
                self.arena.append([])
                for x in range(0, ARENAWIDTH):
                    self.arena[-1].append(0)
                self.arena.reverse()
        
        self.current_tetromino.paint()
        
        if self.current_tetromino.inContact():
            self.placeTetromino()
        
    def draw(self):
        self.screen.fill((0,0,0))
        for y, row in enumerate(self.arena):
            for x, block in enumerate(row):
                drawBlock(x, y, self.screen, self.arena[y][x])
        pygame.display.update()
        
    def mainLoop(self):
        while 1:
            if self.handleEvents() == 1:
                pygame.quit()
                return
            self.update()
            self.draw()
            self.clock.tick(30)
        
def main():
    Game().mainLoop()

main()