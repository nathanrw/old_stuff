#==============================================================================
# writer.py
# Writes text to a surface.
#
#==============================================================================

import pygame
from pygame.locals import *

class ParagraphWriter():
	def __init__(self, font, linelength, lineheight, position, surface, colour):
		self.font = font
		self.linelength = linelength
		self.lineheight = lineheight
		self.position = position
		self.surface = surface
		self.colour = colour
		
	def setup(self,font=None, linelength=None, lineheight=None, position=None, surface=None, colour=None):
		if font is not None:
			self.font = font
		if linelength is not None:
			self.linelength = linelength
		if lineheight is not None:
			self.lineheight = lineheight
		if position is not None:
			self.position = position
		if surface is not None:
			self.surface = surface
		if colour is not None:
			self.colour = colour
			
	def write(self,text):
		charcounter = 0
		linecounter = 0
		last = 0
		lines = []
		while charcounter < len(text):
			if text[charcounter:charcounter+9] == "<ENDLINE>":
				self.surface.blit(self.font.render(text[last:charcounter],1,self.colour),(self.position[0],self.position[1]+linecounter*self.lineheight))
				linecounter+=1
				last = charcounter+9
			charcounter += 1