#==============================================================================
# starfield.py
# Twinkle twinkle little star; how I wonder what you are.
#
#==============================================================================

import pygame
from pygame.locals import *

from random import random as rnd
import random

from maths import *

def fakeColourTemperature(change):
	if change < -0.1:
		return (200,200,255)
	elif change > 0.1:
		return (255,200,200)
	else:
		return (255,255,255)

class Starfield():
	def __init__(self, size, prob):
		self.size = size
		self.stars = []
		for x in range(0,size[0]):
			for y in range(0,size[1]):
				if rnd() < prob:
					self.stars.append([x,y,rnd()])
					
	def draw(self, surface, observer_velocity):
		surface.lock()
		for star in self.stars:
			star[0]-=observer_velocity[0]*0000.1*star[2]
			star[1]-=observer_velocity[1]*0000.1*star[2]
			if star[0] < 0 or star[0] > self.size[0]: star[0] = self.size[0]-star[0]
			if star[1] < 0 or star[1] > self.size[1]: star[1] = self.size[1]-star[1]
			surface.set_at((int(star[0]),int(star[1])),(255,255,255))
		surface.unlock()

class StarfieldDoppler():
	def __init__(self, size, prob):
		self.size = size
		self.stars = []
		for x in range(0,size[0]):
			for y in range(0,size[1]):
				if rnd() < prob:
					self.stars.append([x,y,rnd()])
					
	def draw(self, surface, observer_velocity):
		
		surface.fill((0,0,0))
		
		origin = (surface.get_width()/2, surface.get_height()/2)
		c = 1000
		surface.lock()
		for star in self.stars:
			
			starpos = Sub2DVector(star, origin)
			staraxis = Unit2DVector(starpos)
			
			star_v = -DotProduct2DVector(staraxis, observer_velocity)
			
			# change in wavelength/original wavelength = v/c
			# original = 1 => change = v/c
			
			change = star_v / c
			colour = fakeColourTemperature(change)
			
			star[0]-=observer_velocity[0]*0000.1*star[2]
			star[1]-=observer_velocity[1]*0000.1*star[2]
			if star[0] < 0 or star[0] > self.size[0]: star[0] = self.size[0]-star[0]
			if star[1] < 0 or star[1] > self.size[1]: star[1] = self.size[1]-star[1]
			
			surface.set_at((int(star[0]),int(star[1])),colour)
			surface.set_at((int(star[0])+1,int(star[1])),colour)
			surface.set_at((int(star[0]),int(star[1])+1),colour)
			surface.set_at((int(star[0])+1,int(star[1])+1),colour)
			#pygame.draw.circle(surface, colour, (star[0],star[1]), 1)
		surface.unlock()