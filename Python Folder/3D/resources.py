import pygame, os, sys
from pygame.locals import *
from loadres import *
from load_models import lm

#Load Textures
Bill1_100x100 = basic_import_image("tex.png")
Bill2_100x100 = basic_import_image("tex2.png")
Me = basic_import_image("tex3.png")
Me_25x25 = basic_import_image("tex4.png")
Me_512x512 = basic_import_image("tex6.png")

#Import Models
import md_ship
import md_shiplol

#Load Models
MD_Ship_One = lm(md_ship.faces, md_ship.vertices)
MD_Ship_Two = lm(md_shiplol.faces, md_shiplol.vertices)
