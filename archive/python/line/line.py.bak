#==============================================================================
# line.py
# 2D --> 1D Awesomeness
#
#==============================================================================

import pygame
from pygame.locals import *
from maths import *
import math

pygame.init()

class Line():
	"""
		A line, from start to end and in colour colour.
	"""
	def __init__(self, colour, start, end):
		self.start = start
		self.end = end
		self.colour = colour

def project_line(line, camera_dist, camera_x_overtwo):
	"""
		Project the start and end points of a line onto a line that is
		camera_dist away from the viewpoint and camera_x long.
	"""
	start = Project2DTo1D(line.start, camera_dist, camera_x_overtwo)
	end = Project2DTo1D(line.end, camera_dist, camera_x_overtwo)
	return Line(line.colour, start, end)

def rotate_line_about_point(line, pos, rot):
	"""
		Rotate the start and end points of a line about the given
		point by the given angle.
	"""
	start = Rotate2DVector(Sub2DVector(line.start, pos), rot)
	end = Rotate2DVector(Sub2DVector(line.end, pos), rot)
	return Line(line.colour, start, end)

def rotate_line_about_camera(line, pos, rot):
	"""
		For rendering.
	"""
	new_line = 	Line(line.colour,Sub2DVector(line.start, pos), Sub2DVector(line.end, pos))
	return rotate_line_about_point(new_line, pos, -rot)

class Camera():
	"""
		Stores the position, rotation, length and distance from
		the viewpoint of the camera.
	"""
	def __init__(self, position, rotation, x, d):
		self.position = position
		self.rotation = rotation
		self.x = x
		self.dist = d

lines = [Line((255,0,0),[0,10],[0,-10]),Line((0,255,0),[0,-10],[0,-20])]

screenxy = (800,600)
screen = pygame.display.set_mode(screenxy)
camera = Camera([0,-30],0,screenxy[0],1)

def input():
	"""
		Get input from the user.
	"""
	for e in pygame.event.get():
		if e.type == QUIT:
			pygame.quit()
			return 0
		elif e.type == KEYDOWN:
			if e.key == K_ESCAPE:
				pygame.quit()
				return 0
			elif e.key == K_e:
				camera.rotation += 5*math.pi/180
			elif e.key == K_r:
				camera.rotation -= 5*math.pi/180

def update():
	"""
		Game.
	"""
	pass

def render():
	"""
		Draw to the display surface.
	"""
	
	# Transform lines onto the screen
	rotation = lambda line: rotate_line_about_camera(line,camera.position, \
	camera.rotation)
	projection = lambda line: project_line(line,camera.dist,camera.x*0.5)
	transformed_lines =	map(lambda line:projection(rotation(line)),lines)
	
	screen.fill((0,0,0))
	
	for line in transformed_lines:
		pygame.draw.line(screen, line.colour, [20,line.start*3],[20,line.end*3])
	
	pygame.display.update()

def main():
	"""
		Main loop
	"""
	while 1:
		if input() == 0:
			return 0
		update()
		render()

if __name__ == '__main__':
	main()