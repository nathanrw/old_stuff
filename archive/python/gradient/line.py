import pygame
from pygame.locals import *
from math import sin, cos, hypot, atan2, degrees, ceil
from vector2D import Vector2D
from gradient import transparencyGradient

def tileImageAlongLine(surf, img, start, end):
	
	# Displacement between the two points and its magnitude.
	displacement = Vector2D(start[0]-end[0], start[1]-end[1])
	length = hypot(displacement.x, displacement.y)
	
	# No need to draw anything.
	if length <= 0:
		return
	
	# Save typing it out a lot.
	w = img.get_width()
	h = img.get_height()
	
	# Tile the image along a surface as long as the line.
	
	tiled = pygame.Surface((length, h), SRCALPHA)
	numtiles = int(ceil(length / w))
	
	for x in range(0, numtiles):
		tiled.blit(img, (x*w, 0))
	
	# Get the required angle and rotate the tiled image accordingly.
	angle = atan2(-displacement[1],displacement[0])
	rotated = pygame.transform.rotozoom(tiled, degrees(angle), 1)
	
	# Position the image on the surface it is being drawn to.
	rect = rotated.get_rect()
	rect.center = Vector2D(start) - displacement*0.5
	
	# Draw the finished surface.
	surf.blit(rotated, rect)
	
def main():
	pygame.init()
	screen = pygame.display.set_mode((800,600))
	img = transparencyGradient(100,20,(0,0,0,255))
	while 1:
		for e in pygame.event.get():
			if e.type == QUIT: return
		screen.fill((255,255,255))
		tileImageAlongLine(screen, img, (400,300),pygame.mouse.get_pos())
		pygame.display.update()
	
if __name__ == '__main__':
	main()