#==========================================================================
# Trailer.py
# Because rockets are awesome.
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

class Point():
	def __init__(self):
		self.position = [300,300]
		self.counter = 0
		self.trail = Trail(self)
	def update(self):
		self.counter += 1
		self.position[1] = sin((pi/180)*self.counter) + 300
		self.trail.update()
	def draw(self, surface):
		self.trail.draw(surface)

class PointPair():
	def __init__(self, position, velocity):
		self.velocity = velocity
		self.point1 = [position[0]-1,position[1]-1]
		self.point2 = [position[0]+1,position[1]+1]
		
	def update(self):
		self.point1[0]+=self.velocity[0]
		self.point2[0]+=self.velocity[0]
		self.point1[1]+=self.velocity[1]
		self.point2[1]+=self.velocity[1]

class Trail():
	def __init__(self, obj):
		self.pointpairs = []
	def update(self):
		for pair in self.pointpairs:
			pair.update()
		if len(self.pointpairs) > 10:
			self.addPointPair()
	def addPointPair(self):
		self.pointpairs.append(PointPair(self.obj.position, self.obj.velocity))
		self.pointpairs.remove(self.pointpairs[0])
	def draw(self, surface):
		left = []
		right = []
		for p in self.pointpairs:
			left.append(p.point1)
			right.append(p.point2)
		points = left + right
		pygame.draw.polygon(screen,(255,255,255),points)
		
#==========================================================================
# Setup.
#==========================================================================

pygame.init()

res = (1024,768)
screen = pygame.display.set_mode((res))

point = Point()

#==========================================================================
# Subroutines dependent on the above.
#==========================================================================

def Update():
	point.update()
	point.draw(screen)

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
