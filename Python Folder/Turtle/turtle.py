###############################################################################
# Turtle Game
# turtle.py
# 
# 
# 
###############################################################################

##### Imports #################################################################

import math
import random
import os
import sys
import pygame; from pygame.locals import *

import lib.resource as resource
import lib.maths as maths

from lib.maths import *

import constants

###############################################################################

class NoneSound():
	def __init__(self):
		pass
	def play(self):
		pass

##########
# class Map()
#
# The level.
#
##########

##########
# class GameObject()
# 
# Anything like a projectile, unit, barricade...
# 
##########

class GameObject():
	"""
	
		Represents anything.
	
	"""
	
	anims = None
	sounds = None
	stats = None
	points = None
	
	def __init__(self, position, *groups):
		
		self.groups = []
		for group in groups:
			group.append(self)
			self.groups.append(group)
		
		self.position = position
		
		self.state = "idle"
		
		self.rotation = 0
		
		# If not vector graphics.
		if not self.points:
			
			# Controls the speed of animation.
			self.frameCounter = 0
			self.frameTime = 0
			
			# Points to the current image in the current animation.
			self.animCounter = 0
			
			# Points to the current animation.
			self.currentAnim = self.anims[self.state]
			
			# Length of the current animation, in frames.
			self.currentAnimLength = 0
			
			self.selectAnim()
			self.selectSound()
			
			self.image = self.currentAnim[0]
	
	def addGroup(self, group):
		group.append(self)
		self.groups.append(group)
	
	def removeGroup(self, group):
		group.remove(self)
		self.groups.remove(group)
	
	def changeState(self, state):
		self.state = state
		self.selectAnim()
		self.selectSound()
	
	def selectAnim(self):
		self.currentAnim = self.anims[self.state]
		self.currentAnimLength = len(self.currentAnim)
	
	def selectSound(self):
		if self.sounds.keys().__contains__(self.state):
			self.currentSound = self.sounds[self.state]
		else:
			self.currentSound = NoneSound()
	
	def kill(self):
		for group in self.groups:
			if group.__contains__(self):
				group.remove(self)
	
	def update(self):
		
		# Animate
		
		# Checks that this unit does not use vector graphics.
		if not self.points:
			
			# Time to change the frame?
			if self.frameCounter > self.frameTime:
				
				# Reset the frame counter
				self.frameCounter = 0
				
				# Next frame.
				self.animCounter += 1
				
				# Loop the animation.
				if self.animCounter == self.currentAnimLength:
					self.animCounter = 0
				
				# Get the correct image to draw.
				self.image = self.currentAnim[self.animCounter]
			
			self.frameCounter += 1
		
		# Logic goes here.
	
	def draw(self, surface, view_position):
		
		# If the object does not use vector graphics
		if not self.points:
			
			# Rotate the image according to the rotation of the
			# object.
			image = pygame.transform.rotate(self.image,
			math.degrees(self.rotation))
			
			# Centre the image on the position.
			rect = image.get_rect()
			rect.center = self.position
			
			# Make relative to the camera.
			x = rect.x - view_position[0]
			y = rect.y - view_position[1]
			
			surface.blit(image, (x, y))
		
		# Otherwise, draw a polygon
		else:
			
			points = [] # Temporary list of points
			
			for point in self.points:
				
				# Make the point relative to the camera.
				x = point[0] + self.position[0] - view_position[0]
				y = point[1] + self.position[1] - view_position[1]
				points.append((x, y))
			
			# Draw an outlined polygon
			pygame.draw.polygon(surface, self.colour1, points)
			pygame.draw.lines(surface, self.colour2, 1, points, 2)
	
	def collide(self, obj):
		pass

##########
# class Scenery(GameObject)
#
# Barricades, trees, handcarts...
#
##########

class Scenery(GameObject):
	
	stats = {}
	
	def __init__(self, position, *groups):
		GameObject.__init__(self, position, *groups)
		
		#
		# self.coverBonus = self.stats["coverBonus"]
		# self.health = self.stats["health"]
		# 
		# 
		# 
	
	def collide(self, obj):
		pass
	
	def checkCover(self, unit):
		rect = self.image.get_rect()
		rect.center = self.position
		if rect.collidepoint(unit.position):
			return 1

##########
# class GameUnit(GameObject)
#
# Rabid killer insects, hoomins...
#
##########

class GameUnit(GameObject):
	
	def __init__(self, position, *groups):
		GameObject.__init__(self, position, *groups)
		self.destination = self.position
		
		#
		self.movespeed = 5
		#
	
	def setDestination(self, position):
		self.destination = position
	
	def update(self):
		GameObject.update(self)
		
		displacement = Sub2DVector(self.destination, self.position)
		distance = Magnitude2DVector(displacement)
		if distance > self.movespeed:
			direction = Unit2DVector(displacement)
			move = ScalMul2DVector(direction, self.movespeed)
			self.rotation = math.atan2(move[0], move[1]) + math.pi
			self.position = Add2DVector(self.position, move)

##########
# class Projectile(GameObject)
#
# Bullets and rocks.
#
##########

class Projectile(GameObject):
	stats = {}
	def __init__(self, position, *groups):
		GameObject.__init__(self, position, *groups)


###############################################################################
# Game Data. Stores all images and sounds etc.
###############################################################################

class GameData():
	"""
		Use to keep all resource files handy.
	"""
	
	def __init__(self):
		self.images = resource.ImageController()
		self.sounds = resource.SoundController()
		
		self.font_7 = pygame.font.Font(None, 7)
		self.font_14 = pygame.font.Font(None, 14)
		self.font_24 = pygame.font.Font(None, 24)
		self.font_48 = pygame.font.Font(None, 48)
		
	def loadAll(self, directory):
		"""
			Load all resource files from a directory. Does not like files of
			the same name, even if from multiple directories - the filenames
			must be unique.
		"""
		
		# Associate file extentions with images and sounds.
		image_formats = ("png", "PNG", "jpg", "JPG", "tga", "TGA")
		sound_formats = ("wav", "WAV")
		
		# Get all filenames in the given directory.
		directory = directory + "/"
		filenames = os.listdir("./" + directory)
		
		# Loop over all files in the directory.
		for filename in filenames:
			
			# If the file format is in image_formats, give the filename
			# to the image controller.
			if image_formats.__contains__(filename[-3:]):
				self.images.__setattr__(filename[:-4], \
				directory + filename)
			
			# Else, if the file format is in sound_formats, give the filename
			# to the sound controller.
			elif sound_formats.__contains__(filename[-3:]):
				self.sounds.__setattr__(filename[:-4], \
				directory + filename)

###############################################################################
# Game Class
###############################################################################

class Game():
	
	def __init__(self):
		
		self.camera = Rect(-400,-300,800,600)
		
		# Initialise pygame and pygame.display
		pygame.init()
		self.display = pygame.display.set_mode(self.camera.size)
		pygame.mouse.set_visible(0)
		
		# Sort out time.
		self.clock = pygame.time.Clock()
		self.targetFPS = 60
		
		# Stores all game data, e.g. music + images
		self.data = GameData()
		
		# Show a loading screen while all the data gets loaded can take a while
		self.loadingScreen()
		self.data.loadAll("data")
		
		# Image is drawn to the screen where the cursor would be.
		self.cursor = self.data.images.cursor2
		
		# Groups for game objects.
		self.group_all = []     # Everything.
		self.group_shots = []   # Bullets.
		self.group_units = []   # All units.
		self.group_allies = []  # Owned by the player.
		self.group_enemies = [] # Owned by the horder.
		self.group_scenery = [] # World.
		self.group_selected = []
		
		# Sets up classes for all units.
		self.defineUnits()
		
		# Sets up classes for scenery
		self.defineScenery()
		
		# Stops too many orders being given in one click.
		self.mousecooldown = 10
		self.mousetimer = 0
		
	def loadingScreen(self):
		"""
			Show 'em something to keep 'em happy.
		"""
		
		# Fill screen a nice red colour
		self.display.fill((120,40,40))
		
		# Some nice white size 48 text.
		font = pygame.font.Font(None, 48)
		text = font.render("Loading...", 1, (255,255,255))
		
		# Put it in the top left, and show it.
		self.display.blit(text, (10,10))
		pygame.display.update()
	
	def defineUnit(self, _anims, _sounds, _stats, *groups):
		"""
			Makes a class for a certain type of unit.
			
			If using images rather than vectors set _points to None. Do the
			same to _colour1 and _colour2.
		"""
		class unit(GameUnit):
			
			# For all.
			anims = _anims
			sounds = _sounds
			stats = _stats
			
			# For vector graphics.
			if not _anims.keys.__contains__("idle"):
				points = [(-24,-24),(24,-24),(12,24)]
				colour1 = (100,140,100)
				colour2 = (200,220,200)
			# Else, these are not needed.
			else:
				points = None
				colour1 = None
				colour2 = None
			
			def __init__(self, position):
				GameUnit.__init__(self, position, *groups)
				
		return unit
	
	def defineUnits(self):
		
		_all = self.group_all
		_allies = self.group_allies
		_enemies = self.group_enemies
		_units = self.group_units
		
		class Guardsman(GameUnit):
			anims = {"idle":[self.data.images.guardsman]}
			sounds = {"select":[self.data.sounds.ello,
			self.data.sounds.wat,
			self.data.sounds.wheresmelegs],
			"move":[self.data.sounds.yoh]}
			stats = {}
			def __init__(self, position):
				GameUnit.__init__(self, position, _all, _allies, _units)
		
		self.types_Guardsman = Guardsman
	
	def defineScenery(self):
		
		_scenery = self.group_scenery
		_all = self.group_all
		
		class Bunker(Scenery):
			anims = {"idle":[self.data.images.bunker]}
			sounds = {}
			stats = {}
			def __init__(self, position):
				Scenery.__init__(self, position, _scenery, _all)
				
			def checkCover(self, unit):
				rect = self.image.get_rect()
				rect.center = self.position
				rect.inflate_ip(-120,-120)
				if rect.collidepoint(unit.position):
					return 1
		
		self.types_Bunker = Bunker
		
		class Trench(Scenery):
			anims = {"idle":[self.data.images.trench]}
			sounds = {}
			def __init__(self, position):
				Scenery.__init__(self, position, self.groups_scenery, \
				self.groups_all)
				
		self.types_Trench = Trench
		
		class Mines(Scenery):
			anims = {"idle":[self.data.images.mines]}
			sounds = {}
			def __init__(self, position):
				Scenery.__init__(self, position, self.groups_scenery, \
				self.groups_all)
		
		self.types_Mines = Mines
	
	def run(self):
		"""
			Main loop. Call this.
		"""
		
		self.types_Bunker((0,0))
		self.types_Guardsman((0,0))
		
		while 1:
			
			# Get input from the player.
			if self.getInput() == 0:
				pygame.quit()
				return
			
			# Update all game objects.
			self.update()
			
			# Draw everything to the display
			self.draw()
			
			# Maintain framerate.
			self.clock.tick(self.targetFPS)
	
	def moveScreen(self):
		
		mpos = pygame.mouse.get_pos()
		
		if mpos[0] < 20:
			self.camera.x -= 2
		elif mpos[0] > self.camera.w - 20:
			self.camera.x += 2
		if mpos[1] < 20:
			self.camera.y -= 2
		elif mpos[1] > self.camera.h - 20:
			self.camera.y += 2
	
	def getInput(self):
		"""
			Handles keyboard input etc.
		"""
		for e in pygame.event.get():
			
			# Window has been killed
			if e.type == QUIT:
				return 0
			
			# Keys pressed
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					return 0
			
			# Keys released
			elif e.type == KEYUP:
				pass
		
		self.moveScreen()
		
		if self.mousetimer == 0:
			mouseClick = pygame.mouse.get_pressed()
			
			if mouseClick[0]:
				self.selectUnits()
				self.mousetimer = self.mousecooldown
			if mouseClick[2]:
				self.giveOrders()
				self.mousetimer = self.mousecooldown
		else:
			self.mousetimer -= 1
		return 1
	
	def selectUnits(self):
		
		# Get absolute mouse position
		mpos = pygame.mouse.get_pos()
		
		x = mpos[0] + self.camera.x
		y = mpos[1] + self.camera.y
		
		# Check each friendly unit for selection.
		for unit in self.group_allies:
			
			# Get distance between mouse and unit.
			rel = maths.Sub2DVector(unit.position, (x, y))
			dist = maths.Magnitude2DVector(rel)
			
			if dist < 10:
				
				# Select unit - add it to the group of selected units.
				if not self.group_selected.__contains__(unit):
					random.choice(unit.sounds["select"]).play()
					unit.addGroup(self.group_selected)
				break # Exit the loop - the unit has been found.
			else:
				# Deselect current units.
				if unit.groups.__contains__(self.group_selected):
					unit.removeGroup(self.group_selected)
	
	def giveOrders(self):
		
		# Get absolute mouse position.
		mpos = pygame.mouse.get_pos()
		
		x = mpos[0] + self.camera.x
		y = mpos[1] + self.camera.y
		
		# Determine context.
		
		# Check for an attack order.
		for unit in self.group_enemies:
			
			# Distance from mouse to enemy.
			rel = Sub2DVector(unit.position, (x, y))
			dist = Magnitude2DVector(rel)
			
			if dist < 5: # So player right clicked on an enemy.
				
				return
		
		# A move order.
		for unit in self.group_selected:
			random.choice(unit.sounds["move"]).play()
			unit.setDestination((x, y))
	
	def update(self):
		"""
			Move the game forward.
		"""
		
		# Move everything forward.
		for item in self.group_all:
			
			item.update()
		
		# Determine if units are in cover.
		for unit in self.group_units:
			
			for prop in self.group_scenery:
				
				if prop.checkCover(unit):
					unit.inCover = 1
				else:
					unit.inCover = 0
		
		# Handle collisions.
		for itemOne in self.group_all:
			
			for itemTwo in self.group_all:
				
				if itemOne == itemTwo:
					continue
				
				itemOne.collide(itemTwo)
	
	def draw(self):
		"""
			Put everything on the screen.
		"""
		self.display.fill((100,150,100))
		
		# Draw all GameObjects.
		for item in self.group_scenery:
			item.draw(self.display, (self.camera.x, self.camera.y))
		
		# Draw all units.
		for item in self.group_units:
			item.draw(self.display, (self.camera.x, self.camera.y))
			
			# Show whether units are in cover.
			if item.inCover:
				x = item.position[0] - self.camera.x
				y = item.position[1] - self.camera.y
				pygame.draw.circle(self.display,(200,200,255),(x, y),25,3)
		
		# Draw bullets.
		for item in self.group_shots:
			item.draw(self.display, (self.camera.x, self.camera.y))
		
		# Draw selection circles.
		for item in self.group_selected:
			x = item.position[0] - self.camera.x
			y = item.position[1] - self.camera.y
			pygame.draw.circle(self.display,(200,255,200),(x, y),30,3)
		
		# Draw cursor.
		mousepos = pygame.mouse.get_pos()
		correct_mousepos = (mousepos[0]-2,mousepos[1]-2)
		self.display.blit(self.cursor,correct_mousepos)
		
		# Show.
		pygame.display.update()

###############################################################################

def main():
	game = Game()
	game.run()

if __name__ == '__main__': main()