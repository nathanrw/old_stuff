import pygame
from pygame.locals import *

import math

import numpy

def plotthingy(surf):
	
	centre = surf.get_rect().center
	
	Ox = centre[0]
	Oy = centre[1]
	
	Ux = 0
	Uy = -100
	
	Ax = Ox
	Ay = Oy
	
	srfarry = pygame.surfarray.pixels2d(surf)
	
	for x in xrange(srfarry.shape[0]):
		for y in xrange(srfarry.shape[1]):
			
			Rx = x - (Ax + Ux)
			Ry = y - (Ay + Uy)
			
			R = int(255-(math.hypot(Rx, Ry)))
			if R > 255: R = 255
			if R < 0: R = 0
			srfarry[x,y] = surf.map_rgb(R,R,R)

def main():
	
	pygame.init()
	
	screen = pygame.display.set_mode((300,300))
	
	plotthingy(screen)
	
	pygame.display.update()
	
	pygame.time.wait(5000)

main()