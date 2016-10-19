# 2D Planets
# Damn, docstrings are addictive.
# Needs a tidy up.

import pygame
from pygame.locals import *
import math
from math import cos, sin, radians, pi, sqrt
import random as Random
from random import random

pygame.init()

try:
	import psyco
	psyco.full()
except:
	print "Failed to import psyco."

font = pygame.font.Font(None, 18)

def Noise(x):
	""" Some pseudo-random number function """
	x = (x<<13) ^ x;
	return ( 1.0 - ( (x * (x * x * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

def MakeNoisyCircle(radius, numpoints, magnitude):
	""" Makes a circle and distorts the radius at different values of theta (n). """
	
	angleperpoint = 360.0/numpoints
	points = []
	for n in range(0,numpoints):
		rand = random()
		r = (Noise(int(n*rand*10))*magnitude + radius)
		points.append((r*cos(radians(n*angleperpoint)),r*sin(radians(n*angleperpoint))))
	return points

class Planet():
	""" Class representing a 2D planet. The surface of the planet is represented
		by a circle distored by noise, and mass is approximated from the area of
		the equation for the (normal) circle multiplied by the density of the 
		planet. """
	
	def __init__(self, size, jagginess, density, pos, velocity):
		""" Size: Radius of planet.
			Jagginess: Measure of how noisy the surface looks.
			Density: Density of the material forming the planet. """
		self.points = MakeNoisyCircle(size,int(size/2),jagginess)
		self.density = density
		self.mass = 2*pi*size*density
		self.rotationspeed = 0.1/size
		self.pos = pos
		self.velocity = velocity
		self.rotation = 0
		
	def draw(self,surf, campos):
		""" Draws the planet to the surface given. The middle of the surface is
			the origin (whim). """
		
		ncirc = []
		for point in self.points:
			point = Rotate2DVector(point,self.rotation)
			point = ((int(point[0])+surf.get_width()/2+self.pos[0]+campos[0])/campos[2],(int(point[1])+surf.get_height()/2+self.pos[1]+campos[1])/campos[2])
			ncirc.append(point)
		pygame.draw.polygon(surf,(100,100,100),ncirc)
		pygame.draw.lines(surf,(255,255,255),1,ncirc,2)

	def g(self, obj):
		""" Returns the strength of the gravitational force acting on the given
			object due to the planet. Should be called from the planet on the
			object and from the object on the planet to make it work. """
		rsquared = (((obj.pos[0]-self.pos[0])**2+(obj.pos[1]-self.pos[1])**2))
		return (0.67*self.mass)/rsquared

	def fall(self, obj):
		""" Gravitational interaction between two objects. """

		direction = (obj.pos[0]-self.pos[0],obj.pos[1]-self.pos[1])
		inv_magnitude = 1.0/sqrt(direction[0]**2+direction[1]**2)
		direction = (direction[0]*inv_magnitude,direction[1]*inv_magnitude)
		
		g = obj.g(self)
		self.accelerate((direction[0]*g,direction[1]*g))

	def accelerate(self, amount):
		""" Accelerate the planet by the vector given. """
		
		self.velocity[0] += amount[0]
		self.velocity[1] += amount[1]

	def move(self):
		""" Moves the planet by its velocity. """
		
		self.pos[0] += self.velocity[0]
		self.pos[1] += self.velocity[1]

	def collide(self, obj):
		""" Checks for collisions by comparing the sum of two radii and the
			distance betweem the centres of the two planets.
			"""
		Aradius = len(self.points)*2
		Bradius = len(obj.points)*2
		dist = sqrt(((obj.pos[0]-self.pos[0])**2+(obj.pos[1]-self.pos[1])**2))
		if dist < Aradius + Bradius:
			return 1
	
	def update(self):
		""" Updates planet-specific things. """
		
		self.rotation += self.rotationspeed
		self.move()
		
def Rotate2DVector(vec, angle, origin=[0,0]):
	""" Rotate vec by angle (in radians) about origin. """
	
	sinval = sin(angle)
	cosval = cos(angle)
	
	A = vec[0]-origin[0]
	B = vec[1]-origin[1]
	
	return [A*cosval - B*sinval + origin[0], A*sinval + B*cosval + origin[1]]

class Avatar(Planet):
	""" Used as a base for thiangs such as spaceships and missiles. """
	def __init__(self, pos):
		""" Them thar thrusters be lookin' dodgy. """
		
		self.state = "alive"
		
		self.pos = pos
		self.velocity = [0,0]
		self.mass = 100
		self.density = 0
		self.rotation = 0
		self.points = [[-10,-50],[5,-50],[5,-20],[10,-20],[10,30],[8,30],[12,50],[-12,50],[-8,30],[-12,30],[-12,-20],[-10,-20]]
		
		self.thrusters = []
		
		self.thruster_fore_backward = Thruster(self,[0,-50],[0,1],1)
		self.thrusters.append(self.thruster_fore_backward)
		
		self.thruster_fore_right = Thruster(self,[0,-50],[1,0],1)
		self.thrusters.append(self.thruster_fore_right)
		
		self.thruster_fore_left = Thruster(self,[0,-50],[-1,0],1)
		self.thrusters.append(self.thruster_fore_left)
		
		self.thruster_rear_forward = Thruster(self,[0,50],[0,-1],1)
		self.thrusters.append(self.thruster_rear_forward)
		
		self.thruster_rear_right = Thruster(self,[0,50],[1,0],1)
		self.thrusters.append(self.thruster_rear_right)
		
		self.thruster_rear_left = Thruster(self,[0,50],[-1,0],1)
		self.thrusters.append(self.thruster_rear_left)
		
	def rotate(self,angle):
		""" One line function has one line. Oh, wait. """
		self.rotation += angle
	
	def get_moment(self):
		""" Hmm, dodginess. """
		ACM = (self.thruster_fore_right.strength*self.thruster_fore_right.fraction + \
			self.thruster_rear_left.strength*self.thruster_rear_left.fraction)
		CM  = (self.thruster_fore_left.strength*self.thruster_fore_left.fraction + \
			self.thruster_rear_right.strength*self.thruster_rear_right.fraction)
		return ACM - CM
	
	def update(self):
		""" This comment is entirely useless. """
		for thruster in self.thrusters:
			thruster.thrust()
		self.rotate(-self.get_moment()*(pi/180))
		self.move()
	
class Thruster():
	""" Seemed like a good idea at the time... """
	def __init__(self, object, relative_position, direction, strength):
		""" Object is a reference to whatever's being pushed. """
		self.object = object
		self.position = relative_position
		self.direction = direction
		self.strength = strength
		self.fraction = 0
	def thrust(self):
		""" Called by self.object, whatever it might be. """
		relative_increase = (self.direction[0]*self.strength*self.fraction, self.direction[1]*self.strength*self.fraction)
		absolute_increase = Rotate2DVector(relative_increase,self.object.rotation)
		self.object.accelerate(absolute_increase)
		
class Missile(Avatar):
	""" SHHHWEEEEEWBOOOOOM! """
	def __init__(self,pos, angle, target):
		""" Target is a reference to the target - so it is tracked. """
		self.pos = pos
		self.rotation = angle
		self.target = target
	def update(self):
		""" Missile tries to move towards target using its thrusters, """
		pass
					
def RandomPlanet(pos):
	""" Generate a random bit of rock anwhere within 2000 square...squares of pos. """
	return Planet(Random.randrange(8,12),random()*2,random()*5,[Random.randrange(-1000+pos[0],1000+pos[0]),Random.randrange(-1000+pos[1],1000+pos[1])],[0,0])

def DrawVelocity(vel, surface):
	""" WATCH OUT FOR SPEED CAMERAS! """
	origin = (surface.get_width()/2,surface.get_height()/2)
	vel_pt = (origin[0]+vel[0]*1,origin[1]+vel[1]*1)
	pygame.draw.line(surface,(100,255,100),origin,vel_pt, 3)

def WriteLine(text, pos, surface):
	""" Write LINE? ME WANTS PARAGRAPHS! """
	surface.blit(font.render(text,1,(255,255,255)),pos)

def main():
	""" Fun. """
	print "1024x768 WINDOWED: 1"
	print "1680x1050 FULLSCREEN: 2"
	res = input("Choose: ")
	if res == 1:
		screen = pygame.display.set_mode((1024,768))
	elif res == 2:
		screen = pygame.display.set_mode((1680,1050), FULLSCREEN)
	else:
		print "YOU'RE DOING IT WRONG"
		return
	planets = []
	fx = []
	
	for x in range(0,25):
		planets.append(RandomPlanet([0,0]))
	
	#planets.append(Planet(200,5,2.0,[0,0],[0,0]))
	#planets.append(Planet(20,5,2.0,[-300,0],[0,2.5]))
	
	avatar = Avatar([0,0])
	
	ships = []
	
	planets.append(avatar)
	ships.append(avatar)

	Clock = pygame.time.Clock()
	
	campos = [-avatar.pos[0],avatar.pos[1],1]
	
	gameover = 0
	
	fillcol = (0,0,0)
	
	def CombinePlanets(PlanetA, PlanetB):
		numpoints = len(PlanetA.points)+len(PlanetB.points)
		size = (len(PlanetA.points)+len(PlanetB.points))*2
		density = (PlanetA.density+PlanetB.density)/2.0
		pos = [PlanetA.pos[0]+PlanetB.pos[0]/2,PlanetA.pos[1]+PlanetB.pos[1]]
		velocity = [PlanetA.velocity[0]+PlanetB.velocity[0]/10,PlanetA.velocity[1]+PlanetB.velocity[1]/10]
		
		PlanetA.points = MakeNoisyCircle(size, numpoints, 2)
		PlanetA.density = density
		PlanetA.mass += Oplanet.mass
		PlanetA.velocity = velocity
		PlanetA.rotationspeed = 0.1/size

	while 1:
		spacecol = int(sqrt(avatar.velocity[0]**2+avatar.velocity[1]**2))
		if spacecol > 255:
			spacecol = 255
		fillcol = (spacecol,spacecol,spacecol)
		screen.fill(fillcol)
		
		#Update everything.
		for Aplanet in planets:
			for Oplanet in planets:
				if Oplanet != Aplanet:
					Aplanet.fall(Oplanet)
					if Aplanet.collide(Oplanet) == 1:
						
						# Kill the avatar, should it crash.
						if Aplanet == avatar or Oplanet == avatar:
							avatar.state = "dead"
							avatar.velocity = [0,0]
						
						CombinePlanets(Aplanet,Oplanet)
						planets.remove(Oplanet)
						
			Aplanet.update()
			campos = [-avatar.pos[0]+screen.get_width()*((campos[2]-1)/2.0),-avatar.pos[1]+screen.get_height()*((campos[2]-1)/2.0),campos[2]] 
			Aplanet.draw(screen, campos)
		
		##
		
		if len(planets) < 25:
			planets.append(RandomPlanet([int(avatar.pos[0]),int(avatar.pos[1])]))
		
		##
		
		#Handle input
		if avatar.state == "alive":
			DrawVelocity(avatar.velocity,screen)
		
		for event in pygame.event.get():
			
			if event.type == QUIT:
				pygame.quit()
				return
			
			elif event.type == KEYDOWN:
				
				if event.key == K_ESCAPE:
					pygame.quit()
					return
				
				if avatar.state == "alive":
					if event.key == K_w:
						avatar.thruster_rear_forward.fraction = 0.1
					if event.key == K_s:
						avatar.thruster_fore_backward.fraction = 0.05
					if event.key == K_a:
						avatar.thruster_rear_left.fraction = 1
						avatar.thruster_fore_right.fraction = 1
					if event.key == K_d:
						avatar.thruster_rear_right.fraction = 1
						avatar.thruster_fore_left.fraction = 1
					if event.key == K_e:
						campos[2]+= 0.1
					if event.key == K_r:
						campos[2]-= 0.1
				
			elif event.type == KEYUP:
				
				if avatar.state == "alive":
					if event.key == K_w:
						avatar.thruster_rear_forward.fraction = 0
					if event.key == K_s:
						avatar.thruster_fore_backward.fraction = 0
					if event.key == K_a:
						avatar.thruster_rear_left.fraction = 0
						avatar.thruster_fore_right.fraction = 0
					if event.key == K_d:
						avatar.thruster_rear_right.fraction = 0
						avatar.thruster_fore_left.fraction = 0
						
		WriteLine("2D Planets Thing",(5,5),screen)
		WriteLine("W,S: Fore and aft thrusters.",(5,20),screen)
		WriteLine("A,D: Rotate left and right",(5,35),screen)
		WriteLine("ESC: Quit.",(5,50),screen)
		WriteLine("--------------------------------------------------------",(5,65),screen)
		WriteLine("Current Position: " + str(int(avatar.pos[0])) + "," + str(int(avatar.pos[1])),(5,80),screen)
		WriteLine("Current Velocity: " + str(int(avatar.velocity[0])) + "," + str(int(avatar.velocity[1])),(5,95),screen)
		WriteLine("Fraction of lightspeed: " + str(sqrt(avatar.velocity[0]**2+avatar.velocity[1]**2)/255),(5,110),screen)
		WriteLine("FPS: " + str(int(Clock.get_fps())),(5,125),screen)
		WriteLine("--------------------------------------------------------",(5,140),screen)
		WriteLine("Try not to get killed. Heh.",(5,155),screen)
				
		Clock.tick(60)
		pygame.display.update()

main()