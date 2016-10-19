#==============================================================================
# gui.py
# Clicky clicky drag and drop
#
#==============================================================================

import pygame
from pygame.locals import *

import simple

pygame.init()

simple.defaultStyle.init(simple.gui)
desktop = Desktop()

def main():
	labelStyleCopy = simple.gui.defaultLabelStyle.copy()
	label = Label(position = (50,60),size = (200,100), parent = desktop, text = "Click the button for a proverb!", style = labelStyleCopy)
	
	print "Testing"
if __name__ == '__main__': main()