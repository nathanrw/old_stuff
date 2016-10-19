#==============================================================================
# enemies.py
# The coming of the terrible thinking machines.
# 
#==============================================================================

import pygame
from pygame import *

import math

from random import random as rnd, randrange
rndint = lambda : randrange(-50,51)
rndcol = lambda : (randrange(0,255),randrange(0,255),randrange(0,255))
_rndsign = lambda r: (r >= 0.5) - (r < 0.5)
rndsign = lambda : _rndsign(rnd)

from maths import *
from particles import Explosion

#==============================================================================

class Entity():
	def __init__(self, shipslist, planetslist, fxlist, position):
		self.list = shipslist
		self.food = planetslist
		self.splosions = fxlist
		
		#======================================================================
		
		self.pos = position
		self.velocity = [0,0]
		self.acceleration = [0,0]
		
		#======================================================================
		
		self.energy = 100 #c^2 is left out - this is the equivalent mass
		
		#======================================================================
		
		self.dots = map(lambda x: [rndint(),rndint(),rndint()],range(0,randrange(3,6)))
		self.dotangle = [0.0,0.0,0.0]
		self.dotspin = [rndsign()*rnd()*piby180,rndsign()*rnd()*piby180,rndsign()*rnd()*piby180]
		
		self.colour = [255,255,255]
		
		self.size = self.energy/33
		
		#======================================================================
		
		self.target = None
		
		#======================================================================
		
		self.state = "alive"
		
		#======================================================================
		
		self.ai_counter = 0
		self.ai_rate = 6
		
		self.onscreen = 0
	
	def movedots(self):
		self.dotangles = Add3DVector(self.dotangle, self.dotspin)
		if self.dotangles[0] > 2*pi:
			self.dotangles[0] = 0
		if self.dotangles[1] > 2*pi:
			self.dotangles[1] = 0
		if self.dotangles[2] > 2*pi:
			self.dotangles[2] = 0
		self.dots = map(lambda point: Rotate3DVector(point, self.dotangles), self.dots)
	
	def collide(self, object):
		if (self.size + object.radius) > Distance1DPoints2D(self.pos,object.pos):
			return 1
		return 0
	
	def replicate(self, food):
		if self.energy > 200:
			self.energy -= 100
			pos = Add2DVector(self.pos,[rndsign()*rnd()*food.radius, rndsign()*rnd()*food.radius])
			replica = Entity(self.list,self.food, self.splosions, pos)
			replica.velocity = [rndsign()*rnd()*5,rndsign()*rnd()*5]
			self.list.append(replica)
			self.replicate(food)
		self.size = self.energy/33
	
	def check_for_food(self):
		for object in self.food:
			if self.collide(object):
				if len(object.thrusters) == 0:
					if self.onscreen:
						self.splosions.append(Explosion((object.pos[0],object.pos[1]), object.radius, self.splosions, (200,200,255)))
					self.food.remove(object)
					self.energy += object.mass
					self.replicate(object)
			
			if self.target is not None:
				if Distance1DPoints2D(object.pos, self.pos) < Distance1DPoints2D(self.target.pos, self.pos):
					self.target = object
			if self.target is None:
				self.target = object
	
	def ai(self):
		if self.ai_counter == self.ai_rate:
			self.ai_counter = 0
			self.check_for_food()
			if self.target is not None:
				self.acceleration = ScalMul2DVector(Unit2DVector(Sub2DVector(self.pos,self.target.pos)),-0.1)
		
		self.ai_counter += 1
		
	def move(self):
		self.velocity = Add2DVector(self.velocity,self.acceleration)
		self.pos = Add2DVector(self.pos,self.velocity)
	
	def update(self):
		self.ai()
		self.move()
		
	def draw(self, surface, campos):
		self.onscreen =  clip_pos_to_screen(self.pos[0], self.pos[1], campos, surface.get_width(), surface.get_height())
		if not self.onscreen:
			return
		self.movedots()
		projectdot = lambda point: Add2DVector(Project3DTo2D(Add3DVector(point,[0,0,-20*campos[2]]), surface, 200),self.pos)
		projectedpoints = map(projectdot, self.dots)
		
		conv = lambda xy: world_to_screen(xy[0],xy[1],campos,surface.get_width(),surface.get_height())
		
		centre = conv(self.pos)
		
		transformedpoints = map(conv, projectedpoints)
		
		for point in transformedpoints:
			pygame.draw.line(surface, self.colour, point, centre, 2)
		pygame.draw.circle(surface, self.colour, centre, self.size)

def main():
	pass

if __name__ == '__main__':main()
