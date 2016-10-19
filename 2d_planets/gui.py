#==============================================================================
# gui.py
# Clicky clicky drag and drop
#
#==============================================================================

import pygame
from pygame.locals import *

from maths import *

class GUI():
	def __init__(self, elements):
		self.elements = elements
	def draw(self):
		for func in self.elements:
			func()

def PercentageBar(position, size, percentage, surface, colour, font, text="PercentageBar"):
	pygame.draw.rect(surface,(100,100,100),Rect(position,size))
	pygame.draw.rect(surface, (150,150,150), Rect(position,size). inflate(-4,-4))
	pygame.draw.rect(surface, colour, Rect(position,(int(size[0]*percentage/100),size[1])). inflate(-4,-4))
	pygame.draw.rect(surface,(255,255,255),Rect(position,(int(size[0]*percentage/100),size[1]/2)).inflate(-8,-8))
	words = font.render(text,1,(0,0,0))
	surface.blit(words,(position[0]+(size[0]/2-words.get_width()/2),position[1]+(size[1]/2-words.get_height()/2)))

def GlossBar(position, size, surface, colour, font, text="GlossBar"):
	PercentageBar(position, size, 100, surface, colour, font, text)
	
def MiniMap(position, size, items, reference, surface, font, text="MiniMap"):
	""" Ye're off the edge o' the map, Jack. Here there be pixels! """
	
	pygame.draw.rect(surface, (100,100,100), Rect(position, size))
	pygame.draw.rect(surface, (150,150,150), Rect(position, size).inflate(-4,-4))
	pygame.draw.rect(surface,(225,225,225),Rect(position,(size[0],19)).inflate(-8,-8))
	
	pygame.draw.rect(surface, (200,255,200), Rect(Add2DVector(position, [0,15]), size).inflate(-8,-38))
	pygame.draw.rect(surface,(255,255,255),Rect([position[0],position[1]+19+13],(size[0],19)).inflate(-10,-8))
	
	PercentageBar(position, (size[0],30), 100, surface, (200,255,200), font, text)
	
	colours = ((0,0,255),(255,0,0),(255,255,255),(255,255,0),(255,0,255))
	scale = 20000
	colour = colours[0]
	
	def PositionOnMap(item):
		relative_position = Sub2DVector(item.pos,reference)
		if -scale*0.5 < relative_position[0] < scale*0.5 and -scale*0.5 < relative_position[1] < scale*0.5 :
			map_x = relative_position[0] / scale * (size[0]-16) + size[0]/2 + position[0] + 0
			map_y = relative_position[1] / scale * (size[1]-38) + size[1]/2 + position[1] + 15
			pygame.draw.circle(surface, colour, (map_x,map_y), 2)
	
	for x, group in enumerate(items):
		colour = colours[x]
		map(PositionOnMap, group)
	
def main():
	print "Testing"
if __name__ == '__main__': main()