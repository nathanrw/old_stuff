import os, pygame
from pygame.locals import *
from random import randrange
from Main import tilesize
import LevelGenerator

maps = []

def AddMap(x,y,terrain,tilesize):
    maps.append(LevelGenerator.Level(x,y,terrain,tilesize)
