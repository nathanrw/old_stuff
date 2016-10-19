import pygame, os, sys
from pygame.locals import *
from loadres import *
from load_models import lm

#Load Textures

#Import Models
import md_ship
import md_shiplol
import md_turret

#Load Models
MD_Ship_One = lm(md_ship.faces, md_ship.vertices)
MD_Ship_Two = lm(md_shiplol.faces, md_shiplol.vertices)

MD_Turret_One = lm(md_turret.faces, md_turret.vertices)