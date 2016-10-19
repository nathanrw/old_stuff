#==============================================================================
# 2D Planets
# DEPTH? WHO NEEDS DEPTH?!
#
# What is to be done:
#
#  -> Make planetary collisions work.
#  -> Lasers.
#  -> More UI (No ugly stat printer thing).
#  -> Stuff I've forgotten.
#  -> More than vector graphics?
#  -> ???
#  -> Profit.
#
#==============================================================================

#==============================================================================
# Imports
#==============================================================================

import pygame
from pygame.locals import *

import math
from math import cos, sin, radians, pi, sqrt, atan, degrees

import random as Random
from random import random

try:
	import psyco
	psyco.full()
except:
	print "Failed to import psyco."

#==============================================================================
# My own:
#==============================================================================

from planet import Planet, RandomPlanet
from maths import *
from noise import MakeNoisyCircle
from writer import ParagraphWriter
from avatar import Avatar
from thruster import Thruster
from missile import Missile
from particles import AffixedEmitter
from starfield import Starfield, StarfieldDoppler
from gui import PercentageBar, MiniMap, GUI
from enemies import Entity

#==============================================================================
# Setup.
#==============================================================================

if raw_input("Use defaults, Y/N: ")=="N":
	width = input("Screen width: ")
	height = input("Screen height: ")
	full = raw_input("Fullscreen, Y/N: ")=="Y"
else:
	width = 1024
	height = 768
	full = 0

try:
	if full:
		screen = pygame.display.set_mode((width,height), FULLSCREEN)
	else:
		screen = pygame.display.set_mode((width,height))
except:
	print "YOU FAIL"

#==============================================================================

fillcol = (0,0,0) 	# Background.

#==============================================================================

planets = [] 		# Misnomer - everything affected by gravity.
fx = [] 			# Pretty effects which don't do anything.
ships = [] 			# The player, other ships.

#==============================================================================

pygame.init()
font = pygame.font.Font(None, 18)
Clock = pygame.time.Clock()

#==============================================================================

writer = ParagraphWriter(font, 400, 15, (5,5),	# Writes stats to screen.
						screen, (255,255,255))

#==============================================================================

gameover = 0 # Set to one when the player is dead.
campos = [0,0,1] # Position of the camera. [2] is the zoom level.
zooming = 0 # Zoomeh

#==============================================================================

calcpersecond = 1	# Number of gravity iterations per
calccounter = 0		# iteration of the main loop.

#==============================================================================

avatar = Avatar([0,0]) # The player's ship.

planets += map(lambda x: RandomPlanet([0,0],200),	# Add some random planets to
				range(0,25)) + [avatar]				# planets.

ships += [avatar]	# Add a reference to the player to ships.

fx += map(lambda thruster: AffixedEmitter(thruster,3),	# Add references to the
			avatar.thrusters)							# avatar rockets to fx.

#==============================================================================

starfield = StarfieldDoppler((screen.get_width(),	# Create a starfield for the
					screen.get_height()),	# background. 3rd parameter is
					0.0005)					# the probability of any one pixel
											# being a star.

#==============================================================================

barwidth = 200
barx = screen.get_width()-barwidth-30

## Percentage Bars

# Health of the avatar.
healthBar = lambda: PercentageBar((barx,30),(200,30),100*avatar.hull,screen, \
(255,200,200), font, "Hull Integrity")

#Fuel of the avatar.
fuelBar = lambda: PercentageBar((barx,90),(200,30),100*avatar.reactionmass,\
screen, (200,200,255), font, "Reaction Mass")

# The minimap
miniMap = lambda : MiniMap((barx, 150), (barwidth,barwidth+38), [planets, \
ships, [avatar]], avatar.pos, screen, font, "Sensors")

GUI_Elements = [healthBar, fuelBar, miniMap]
Interface = GUI(GUI_Elements)

#==============================================================================
#==============================================================================
#==============================================================================
# Experimental
#==============================================================================

for x in range(0,10):
	ships.append(Entity(ships, planets, fx, [x*10 + 200,x*10 + 200]))


#==============================================================================
# /Experimental
#==============================================================================
#==============================================================================
#==============================================================================

#==============================================================================
# GUI
#==============================================================================

def DrawGui():
	Interface.draw()

#==============================================================================
# Update everything.
#==============================================================================

def Update():
	global calccounter
	
	starfield.draw(screen,avatar.velocity)
	
	# Update orbitty stuff.
	screen.lock()
	for P1 in planets:
		for P2 in planets:
			if P1 != P2:
				P1.fall(P2)
				if P1.collide(P2):
					if P1 == avatar or P2 == avatar:
						avatar.state = "dead"
					planets.remove(P2)
		P1.update()
		P1.draw(screen, campos)
		if P1.state == "dead":
			planets.remove(P1)
	screen.unlock()
	
	if avatar.reactionmass < 1.0:
		avatar.reactionmass += 0.0001
		avatar.mass += 0.0001
	
	# Update effects.
	for effect in fx:
		effect.draw(screen,campos)
		if effect.state == "dead":
			fx.remove(effect)
	
	# Update ships.
	for ship in ships:
		if ship != avatar:
			ship.update()
			ship.draw(screen, campos)
		if ship.state == "dead":
			ships.remove(ship)
	
	# Update the camera.
	campos[0] = -avatar.pos[0] + (screen.get_width())*((campos[2]-1)*0.5) \
	- avatar.velocity[0]
	campos[1] = -avatar.pos[1] + (screen.get_height())*((campos[2]-1)*0.5) \
	- avatar.velocity[1]
	
	# Spawn planets.
	if len(planets) < 25:
		planets.append(RandomPlanet([int(avatar.pos[0]),int(avatar.pos[1])],\
		18))
	
	# Targetting.
	if avatar.state == "alive":
		origin = (screen.get_width()/2,screen.get_height()/2)
		if avatar.target != 0:
			X = int((avatar.target.pos[0]+screen.get_width()/2+campos[0]) \
			/(campos[2]+0.0001))
			Y = int((avatar.target.pos[1]+screen.get_height()/2+campos[1]) \
			/(campos[2]+0.0001))
			pygame.draw.line(screen,(255,100,100),origin,(X,Y),2)
	
	DrawGui()

#==============================================================================
# Input
#==============================================================================

class PlanetFinder():
	def __init__(self, xy):
		self.radius = 40
		self.pos = [xy[0],xy[1]]

def GetInput():
	global zooming
	for event in pygame.event.get():
		
		if event.type == QUIT:
			return 0
		
		elif event.type == KEYDOWN:
			
			if event.key == K_ESCAPE:
				return 0
			
			if not gameover:
				if event.key == K_w:
					avatar.thruster_rear_forward.fraction = 0.5
				if event.key == K_s:
					avatar.thruster_fore_backward.fraction = 0.3
				if event.key == K_a:
					avatar.thruster_rear_left.fraction = 0.1
					avatar.thruster_fore_right.fraction = 0.1
				if event.key == K_d:
					avatar.thruster_rear_right.fraction = 0.1
					avatar.thruster_fore_left.fraction = 0.1
			
		elif event.type == KEYUP:
			
			if not gameover:
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
		
		elif event.type == MOUSEBUTTONDOWN:
			
			if not gameover:
				
				# Fire missile at target
				if event.button == 1:
					if avatar.target != 0:
						if avatar.reactionmass >= 0.1:
							
							missile = Missile(Add2DVector(avatar.pos,\
							Rotate2DVector([0,-70],avatar.rotation)),\
							avatar.velocity,avatar.rotation,avatar.target)
							
							planets.append(missile)
							
							avatar.reactionmass -= 0.1
							avatar.mass -= 0.1
							
							for thruster in missile.thrusters:
								fx.append(AffixedEmitter(thruster, 3))
						
						else:
							avatar.reactionmass = 0
				
				# Aquire target
				elif event.button == 2:
					screenXY = pygame.mouse.get_pos()
					
					worldX = screenXY[0]*campos[2]-(campos[0]+0.5*\
					screen.get_width())
					
					worldY = screenXY[1]*campos[2]-(campos[1]+0.5*\
					screen.get_height())
					
					worldXY = PlanetFinder((worldX,worldY))
					
					for obj in planets:
						if obj.collide(worldXY,0):
							if obj != avatar:
								avatar.aquire_target(obj)
							break
					
				# Cancel target
				elif event.button == 3:
					avatar.aquire_target(0)
				
				# Zoom
				elif event.button == 4:
					campos[2] -= 0.1
				
				# Zoom
				elif event.button == 5:
					campos[2] += 0.1
	return 1

#==============================================================================
# Output some stuff.
#==============================================================================

def PrintStats():
	stats = "2D Planets Thing" + "<ENDLINE>" + \
	"W,S: Fore and aft thrusters." + "<ENDLINE>" + \
	"A,D: Rotate left and right" + "<ENDLINE>" + \
	"ESC: Quit." + "<ENDLINE>" + \
	"--------------------------------------------------------" + "<ENDLINE>" + \
	"Current Position: " + str(int(avatar.pos[0])) + "," + str(int(avatar.pos[1])) + "<ENDLINE>" + \
	"Current Velocity: " + str(int(avatar.velocity[0])) + "," + str(int(avatar.velocity[1])) + "<ENDLINE>" + \
	"Fraction of lightspeed: " + str(sqrt(avatar.velocity[0]**2+avatar.velocity[1]**2)/3000000) + "<ENDLINE>" + \
	"FPS: " + str(int(Clock.get_fps())) + "<ENDLINE>" + \
	"Zoom: " + str(campos[2]) + "<ENDLINE>" + \
	"World Eaters: " + str(len(ships)-1) + "<ENDLINE>" + \
	"--------------------------------------------------------" + "<ENDLINE>" + \
	"Try not to get killed." + "<ENDLINE>"
	writer.write(stats)

#==============================================================================
# Run everything.
#==============================================================================

def main():
	while 1:
		if GetInput() == 0:
			pygame.quit()
			return
		Update()
		PrintStats()
		Clock.tick(30)
		pygame.display.update()

def profile():
	import hotshot
	prof = hotshot.Profile("planets")
	prof.runcall(main)
	prof.close()

if __name__ == '__main__': main()