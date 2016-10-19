#==============================================================================
# particles.py
# n'arrr, thar be nae hadron collider here! Ye be lookin' on th' wrong ship,
# matey!
#==============================================================================

import pygame
from pygame.locals import *

import random
from random import random as rnd

from math import sin, cos

from maths import *

#==============================================================================
# Emitters
#==============================================================================

class StandardEmitter():
	""" Hmm, does anything actually use this, really? """
	
	state = "alive"
	
	def __init__(self, position, direction, volume):
		
		self.position = position
		self.direction = direction
		self.volume = volume
		self.particles = []
	
	#==========================================================================
	
	def emit(self):
		
		particles = []
		n = 3
		for x in range(0, int(self.volume)):
			
			self.particles.append(Particle(self.position, ScalMul2DVector \
			(Add2DVector(self.direction,[rnd(),rnd()]),n), [0,0], \
			(255,100,255),(100,100,100), 50))

#==============================================================================

class AffixedEmitter(StandardEmitter):
	""" Emitter is affixed to a thruster. """
	
	def __init__(self, obj, volume):
		
		self.obj = obj
		
		StandardEmitter.__init__(self, self.obj.position, Rotate2DVector\
		(self.obj.direction, self.obj.object.rotation), volume)

	#==========================================================================

	def emit(self):
		
		particles = []
		n = 3
		
		for x in range(0, int(self.volume)):
			vel = ScalMul2DVector(Add2DVector(self.direction,\
			[rnd()/4,rnd()/4]),n)
			
			vel[1] = -vel[1]
			vel[0] = -vel[0]
			vel = Add2DVector(vel,self.obj.object.velocity)
			
			self.particles.append(Particle(self.position, vel, [0,0], \
			(100+int(rnd()*155),100+int(rnd()*155),255),(0,0,0), 100))
	
	#==========================================================================
	
	def draw(self, surf, campos):
		
		if self.obj.state == "dead" and len(self.particles) == 0:
			self.state = "dead"
			
		self.position = Add2DVector(self.obj.object.pos,\
		Rotate2DVector(self.obj.position,self.obj.object.rotation))
		
		self.direction = Rotate2DVector(self.obj.direction, \
		self.obj.object.rotation)
		
		self.volume = self.obj.fraction*10
		
		if self.obj.state != "dead":
			self.emit()
			
		for particle in self.particles:
			particle.draw(surf, campos)
			
			if particle.state == "dead":
				self.particles.remove(particle)

#==============================================================================

class AffixedCircularEmitter():
	state = "alive"
	def __init__(self, obj, volume, fx):
		self.obj = obj
		self.particles = []
		self.volume = volume
		self.fxlist = fx
	def emit(self):
		for x in range(0, int(self.volume)):
			pass

#==============================================================================
# Effects derived from emitters.
#==============================================================================

class Explosion():
	particles = []
	duration = 4
	counter = 0
	state = "alive"
	def __init__(self, pos, size, fx, colour):
		self.position = pos
		self.radius = size
		self.density = 2*pi*self.radius
		self.colour = colour
		self.fxlist = fx
	def emit(self):
		for x in range(0,self.density/40):
			theta = rnd()*twopi
			vel = [5*cos(theta), 5*sin(theta)]
			self.particles.append(Particle(self.position, vel, [0,0], \
			Sub3DVector(self.colour,[rnd()*100,rnd()*100,rnd()*100]), [0,0,0], 200, 3))
		for x in range(0,self.density/100):
			theta = rnd()*twopi
			vel = [10*cos(theta), 10*sin(theta)]
			self.particles.append(Particle(self.position, vel, [0,0], \
			Sub3DVector(self.colour,[rnd()*20,rnd()*20,rnd()*20]), [100,100,100], 100, 3))
	def draw(self, surf, campos):
		if self.counter < self.duration:
			self.emit()
		for particle in self.particles:
			particle.draw(surf, campos)
			if particle.state == "dead":
				self.particles.remove(particle)
		self.counter += 1
		if len(self.particles) == 0:
			self.fxlist.remove(self)

#==============================================================================
# Particles
#==============================================================================

class Particle():
	colourcounter = 0
	state = "alive"
	
	#==========================================================================
	
	def __init__(self, position, velocity, acceleration, start_colour, \
	end_colour, lifespan, size = 1):
		
		self.position = position
		self.velocity = velocity
		self.acceleration = acceleration
		
		self.size = size
		
		self.colours = []
		step = [0,0,0]
		
		step[0] = (end_colour[0]-start_colour[0])/float(lifespan)
		step[1] = (end_colour[1]-start_colour[1])/float(lifespan)
		step[2] = (end_colour[2]-start_colour[2])/float(lifespan)
		
		for x in range(0, lifespan):
			self.colours.append((int((start_colour[0]+x*step[0])),\
			int((start_colour[1]+x*step[1])),int((start_colour[2]+x*step[2]))))
		
		self.lifespan = lifespan
	
	#==========================================================================
	
	def draw(self, surf, campos):
		
		if not clip_pos_to_screen(self.position[0], self.position[1], \
		campos, surf.get_width(), surf.get_height()):
			return
		
		if self.colourcounter < self.lifespan:
			
			size = int(1+(8.0/campos[2]))*self.size
			
			point = ((surf.get_width()/2+self.position[0]+campos[0])/campos[2],\
			(surf.get_height()/2+self.position[1]+campos[1])/campos[2])
			
			pygame.draw.rect(surf,self.colours[self.colourcounter],\
			Rect(point[0]-2,point[1]-2,size,size))
			
			self.velocity = Add2DVector(self.velocity, self.acceleration)
			self.position = Add2DVector(self.position, self.velocity)
			
			self.colourcounter+=1
			
		elif self.colourcounter >= self.lifespan: self.state="dead";
		
class Particle2():
	state = "alive"
	counter = 0
	animcounter = 0
	
	def __init__(self, position, velocity, acceleration, lifespan, size=4, \
	colours=((255,255,255),(255,255,255)), images=None):
		
		self.position = position
		self.velocity = velocity
		self.acceleration = acceleration
		self.size = size
		
		self.step = Mul3DVector(Sub3DVector(colours[1],colours[0]),1.0/lifespan)
		self.colour = [colours[0][0],colours[0][1],colours[0][2]]
		
		self.images = images
		
		self.lifespan = lifespan
	
	def draw(self, surf, campos):
		
		if not clip_pos_to_screen(self.position[0], self.position[1], \
		campos, surf.get_width(), surf.get_height()):
			return
		
		if self.counter < self.lifespan:
			
			size = int(1+(8.0/campos[2]))*self.size
			
			point = world_to_screen(position[0],position[1],campos,\
			screen.get_width(),screen.get_height())
			
			if self.images is not None:
				img = self.images[animcounter]
			
			else:
				pass

class AngularParticle():
	lifecounter = 0
	state = "alive"
	
	#==========================================================================
	
	def __init__(self, group, r, outward, theta, omega, origin, velocity,\
	start_colour, end_colour, lifespan) :
		self.group = group
		
		
		self.r = r
		self.theta = theta
		self.omega = omega
		self.origin = origin
		self.outward = outward
		self.velocity = velocity
		
		
		l = 1.0/lifespan
		self.step = Mul3DVector(Sub3DVector(end_colour,start_colour),l)
		self.lifespan = lifespan
		
		self.colour = self.start_colour
		
	#==========================================================================
		
	def draw(self, surface, campos):
		
		displacement = ( self.r*cos(self.theta), self.r*sin(self.theta) )
		position = Add2DVector(self.origin, displacement)

		
		self.theta += self.omega
		self.r += self.outward
		self.origin = Add2DVector(self.origin, self.velocity)

		
		if not clip_pos_to_screen(displacement[0], displacement[1], \
		campos, surf.get_width(), surf.get_height()):
			return

		
		point = world_to_screen(position[0],position[1],campos,\
		screen.get_width(),screen.get_height())
		
		size = int(1+8/campos[2])
		
		self.colour = Add3DVector(self.colour,self.step)
		
		pygame.draw.rect(surf,colour,Rect(point[0]-2,point[1]-2,size,size))

		
		self.lifecounter += 1
		if self.lifecounter == self.lifespan:
			self.group.remove(self)
