#==========================================================================
# Barebones.py
# A bare bones pygame program.
# For great justice.
#==========================================================================

#==========================================================================
# Imports
#==========================================================================

import pygame
from pygame.locals import *

import math
from math import sqrt, sin, cos, radians, pi

import random

try:
	import psyco
	psyco.full()
except:
	print "Cannot use psyco."

#==========================================================================
# General subroutines.
#==========================================================================

### Insert code here

#==========================================================================
# Classes.
#==========================================================================

### Insert code here

#==========================================================================
# Setup.
#==========================================================================

pygame.init()

res = (1024,768)
screen = pygame.display.set_mode((res))

#==========================================================================
# Subroutines dependent on the above.
#==========================================================================

def Update():
	pass

def Input():
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			return 0
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				return 0
	return 1

#==========================================================================
# Run everything.
#==========================================================================

def main():
	while 1:
		Update()
		if Input() == 0:
			return
		pygame.display.update()

if __name__ == '__main__': main()
