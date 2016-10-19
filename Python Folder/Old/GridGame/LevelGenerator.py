#Floor Generation Thing

import os, pygame

from random import randrange
from pygame.locals import *
from LoadRes import ImportImg

class Level():
    def __init__(self,x,y,terrain,tilesize):
        self.x = x
        self.y = y
        self.terrain = terrain # Thy terrain types MUST be integers.
        self.tilesize = tilesize
        
        self.grid = self.LevelGen()
        self.terrainimgs = self.ImgLoad()
        self.Map = self.MapMaker()

    def LevelGen(self):
        Grid = []
        for x in xrange(self.x*self.y):
            Grid.append(self.terrain[randrange(0,len(self.terrain))])
        return Grid

    def ImgLoad(self):
        for name in self.terrain:
            terrainimgs = []
            terrainimgs.append(ImportImg(name,"maptile"))
        return terrainimgs

    def MapMaker(self):
        Map = pygame.Surface((self.x*self.tilesize,self.y*self.tilesize))
        CounterX = 0
        CounterY = 0
        Cell = 0
        while CounterY < self.y:
            while CounterX < self.x:
                Map.blit(self.terrainimgs[self.grid[Cell]],
                         (CounterX,CounterY)
                         )
                CounterX += 1
                Cell += 1
            CounterY += 1

        return Map
