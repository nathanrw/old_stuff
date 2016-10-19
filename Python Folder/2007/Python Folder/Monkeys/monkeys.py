##############################################################################
# ATTENTION  WILD BILL LOVES  AND HE WILL KILL  WITH A HUGE  I'M NOT FUCKING #
#   HAHAR     THIS DOCUMENT     ANY TAMPERER       STICK         KIDDING     #                                                                            #
##############################################################################
#                               LOL NOOB. JK.                                #
##############################################################################

print "Importing Modules"

# Importation ################################################################
#### Well, Duh ###############################################################

import pygame, os, math
from pygame.locals import *
from math import *

# Print Shit To Console ######################################################
#### Well, Why Not? ##########################################################

print "..."
print "Import Finished"
print "..."
print "Defining Classes And Functions"

# Useful Functions And Classes ###############################################
#### Visual Effects ##########################################################

def screenfade(screen, inout):

    if inout == 1:
        col1 = 200
        col2 = 200
        col3 = 200
    elif inout == 0:
        col1 = 0
        col2 = 0
        col3 = 0
        
    counter = 0
    
    while counter < 40:
                
        screen.fill((col1, col2, col3))
        pygame.display.flip()
        pygame.display.update()

        if inout == 1:
            col1 = col1 - 5
            col2 = col2 - 5
            col3 = col3 - 5
        elif inout == 0:
            col1 = col1 + 5
            col2 = col2 + 5
            col3 = col3 + 5
            
        if counter < 40:
            counter = counter + 1
        pygame.time.delay(30)

def splashscreen(screen):
    background_image, background_rect = load_image("splashscreen.bmp")
    screen.blit(background_image, (0, 0))
    pygame.display.update()
    pygame.display.flip()

# Useful Functions ###########################################################
#### Loady Functions #########################################################

def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

def load_sound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound()
	fullname = os.path.join('data', name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error, message:
		print 'Cannot load sound:', fullname
		raise SystemExit, message
	return sound

print "..."
print "Classes Defined"
print "..."
print "Doing Misc Things"

# Random Things ##############################################################
#### Can't Think Of Another Category #########################################

print "..."
print "Misc Things Done"
print "..."
print "Running Main Program"

# Main Functions #############################################################
#### YEAH! ###################################################################

def intro():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("THIS IS BUT AN INTRO!")

    screenfade(screen, 0)
    splashscreen(screen)
    pygame.time.delay(1700)
    screenfade(screen, 1)
    pygame.time.delay(30)


def main():

    intro()
    
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("BEHOLD, THE MONKEYLORD!")

    pygame.display.update()

    running = 1

    while running == 1:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0

main()

print "Done"

# Program Finished ###########################################################
#### Phew! ###################################################################
