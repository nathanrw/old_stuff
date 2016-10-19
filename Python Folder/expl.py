from vec2d import vec2d

import pygame
from pygame.locals import *

import math

import random

import psyco
psyco.full()

def DefineNewSimpleParticle(durationA, sizeA, startColA, endColA=None):
	if not endColA:
		endColA = startColA
	class NewSimpleParticle(SimpleParticle):
		startCol = startColA
		endCol = endColA
		duration = durationA
		size = sizeA
		def __init__(self, pos, vel, acc, *groups):
			SimpleParticle.__init__(self, pos,vel,acc,*groups)
	return NewSimpleParticle

def DefineNewSimpleEmitter(durationA, *emissionsA):
	class NewSimpleEmitter(Emitter):
		duration = durationA
		def __init__(self, pos, vel, acc, *groups):
			Emitter.__init__(self,pos,vel,acc,*groups)
			for emission in emissionsA:
				self.emissions.append(emission)
	return NewSimpleEmitter

def DefineNewGibbingEmitter(durationA, emissionsA, gibsA):
	class NewGibbingEmitter(GibbingEmitter):
		duration = durationA
		def __init__(self, pos, vel, acc, *groups):
			GibbingEmitter.__init__(self, pos, vel, acc, *groups)
			for emission in emissionsA:
				self.emissions.append(emission)
			for gib in gibsA:
				self.gibs.append(gib)
	return NewGibbingEmitter

class Particle():
	
	duration = 40
	
	def __init__(self, pos, vel, acc, *groups):
		
		self.pos = pos
		self.vel = vel
		self.acc = acc
		
		self.groups = []
		for group in groups:
			group.append(self)
			self.groups.append(group)
		
		self.lifetime = 0
		
	def update(self, dt):
		
		self.lifetime += dt
		if self.lifetime > self.duration:
			self.kill()
		
		self.pos += self.vel*dt
		self.vel += self.acc*dt
		
	def draw(self, surface): pass

	def kill(self):
		for g in self.groups:
			g.remove(self)

class SimpleParticle(Particle):
	
	startCol = (100,100,100)
	endCol = (0,0,0)
	duration = 300
	size = 2
	
	def __init__(self, pos, vel, acc, *groups):

		Particle.__init__(self, pos, vel, acc, *groups)

		self.R = self.startCol[0]
		self.G = self.startCol[1]
		self.B = self.startCol[2]
		self.A = 255.0
		
		self.dR_dt = float(self.endCol[0]-self.R)/self.duration
		self.dG_dt = float(self.endCol[1]-self.G)/self.duration
		self.dB_dt = float(self.endCol[2]-self.B)/self.duration
		self.dA_dt = -255.0/math.sqrt(self.duration)
		
		self.alphalim = self.duration - math.sqrt(self.duration)
	def update(self, dt):
		Particle.update(self, dt)
		
		self.R += self.dR_dt * dt
		self.G += self.dG_dt * dt
		self.B += self.dB_dt * dt
		if self.lifetime >=self.alphalim:
			self.A += self.dA_dt * dt
	
	def draw(self, surface):
		
		temp = pygame.Surface((self.size*2,self.size*2))
		rect = temp.get_rect()
		pygame.draw.circle(temp,(self.R,self.G,self.B),rect.center,self.size)
		temp.set_alpha(self.A)
		temp.set_colorkey((0,0,0))
		rect.center=self.pos
		surface.blit(temp, rect)
		#surface.set_at(self.pos, (self.R,self.G,self.B))

class Emitter(Particle):
	
	def __init__(self, pos, vel, acc, *groups):
		Particle.__init__(self, pos, vel, acc, *groups)
		self.particles = []
		self.emissions = []
		self.killed=0
	
	def update(self, dt):
		
		self.lifetime += dt
		
		self.pos += self.vel*dt
		self.vel += self.acc*dt
		
		for particle in self.particles:
			particle.update(dt)
		
		if self.lifetime > self.duration:
			if len(self.particles) == 0:
				self.kill()
				return
			else:
				return
			
		self.emit(dt)
	
	def draw(self, surface):
		for particle in self.particles:
			particle.draw(surface)
	
	def addEmission(self, emission):
		self.emissions.append(emission)
	
	def emit(self, dt):
		for emission in self.emissions:
			emission.emit(dt, self.pos, self.vel, (self.particles))

class GibbingEmitter(Emitter):
	
	def __init__(self, pos, vel, acc, *groups):
		Emitter.__init__(self, pos, vel, acc, *groups)
		self.gibs=[]
		self.killed=0
	def kill(self):
		if not self.killed:
			self.killed = 1
			for gib in self.gibs:
				gib.emit(1, self.pos, self.vel, (self.particles))
		else:
			Particle.kill(self)

class Emission():
	
	def __init__(self, particle, speed, rate, spread, resistance):
		self.particle = particle
		self.speed = speed
		self.rate = rate
		self.spread = spread
		self.resistance = resistance
		
		self.t = 0
		self.timePerEmission = 1.0/rate
	
	def emit(self, dt, pos, vel, *groups):
		self.t += dt
		numEmissions = int(self.t/self.timePerEmission)
		if numEmissions: self.t = 0
		for n in range(0,numEmissions):
			self.spawnParticle(pos, vel, *groups)
	
	def spawnParticle(self, pos, vel, *groups):
		
		alpha = math.atan2(vel.x,vel.y)
		
		theta = random.choice((1,-1))*random.random()*self.spread*0.5 - alpha - math.pi/2
		
		v = vec2d(math.cos(theta)*self.speed,math.sin(theta)*self.speed)
		
		a = v.normalized()*self.resistance
		
		self.particle(vec2d(pos.x,pos.y),v+vel,a,*groups)

class ExplosionGenerator():
	
	def __init__(self):
		
		pygame.init()
		self.screen = pygame.display.set_mode((800,600))
		self.emitters=[]
		
		self.clock = pygame.time.Clock()
	
	def getInput(self):
		
		for e in pygame.event.get():
			if e.type == QUIT:
				return 0
			elif e.type == MOUSEBUTTONDOWN:
				self.spawnEmitter(e.pos)
		return 1
	
	def explosion(self, pos):
	
		newParticle = DefineNewSimpleParticle(10,4,(255,255,200),(0,0,0))
		newParticle2 = DefineNewSimpleParticle(10,1,(255,255,200),(0,0,0))
		newParticle3 = DefineNewSimpleParticle(30,4,(255,255,200),(0,0,0))
		
		particles = Emission(newParticle, 6, 2, 0.2, 0)
		
		particles2 = Emission(newParticle2, 6,2,0.1,0)
		
		particles3 = Emission(newParticle3, 1,2,6.28,0)
		
		particleEmitter2 = DefineNewSimpleEmitter(10, particles3)
		emitters2 = Emission(particleEmitter2,0,2,6.28,0)
		
		particleEmitter3 = DefineNewSimpleEmitter(20, particles3)
		emitters3 = Emission(particleEmitter3,0,2,6.28,0)
		
		particleEmitter = DefineNewGibbingEmitter(30, (particles,),())

		emitters = Emission(particleEmitter, 4, 1, 6.28, 0)
		
		
		explosion = DefineNewSimpleEmitter(6, emitters, emitters2)
		
		explosion(vec2d(pos),vec2d(0,0),vec2d(0,0),self.emitters)
	
	def laserhit1(self, pos):
		
		smallWhiteSpark = DefineNewSimpleParticle(8,1,(255,255,255))
		laserthing = DefineNewSimpleParticle(5,1,(255,255,255))
		smallFireSpark = DefineNewSimpleParticle(4,1,(255,255,255))
		
		smallWhiteSparkShower = Emission(smallWhiteSpark, 3, 3, 3,0)
		beam = Emission(laserthing, 6, 1, 0, 0)
		
		fire = Emission(smallFireSpark, 1, 1, 3.14, 0)
		
		fireEmitter = DefineNewSimpleEmitter(50, fire)
		
		fireEmission = Emission(fireEmitter, 0, 0.4, 6.28, 0)
		
		testEmitter = DefineNewSimpleEmitter(6, beam, smallWhiteSparkShower, fireEmission)
		testEmitter(vec2d(pos), vec2d(0,0), vec2d(0,0), self.emitters)
	
	def spawnEmitter(self, pos):
		self.explosion(pos)
	def update(self, dt):
		for emitter in self.emitters:
			emitter.update(dt)
	
	def draw(self):
		self.screen.fill((150,150,150))
		for emitter in self.emitters:
			emitter.draw(self.screen)
		pygame.display.update()
	
	def mainLoop(self):
		t1 = 0
		t2 = 0
		dt = 0
		while self.getInput():
			dt = t2-t1
			t1 = pygame.time.get_ticks()
			self.update(dt/20.0)
			self.draw()
			t2 = pygame.time.get_ticks()
			self.clock.tick()

ExplosionGenerator().mainLoop()