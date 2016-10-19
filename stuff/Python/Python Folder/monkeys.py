##############################################################################
# ATTENTION  WILD BILL LOVES  AND HE WILL KILL  WITH A HUGE  I'M NOT FUCKING #
#   HAHAR     THIS DOCUMENT     ANY TAMPERER       STICK         KIDDING     #                                                                            #
##############################################################################
#             LOL NOOB. JK.  MADE BYE NATHAN WOODWARD, WHO WINS              #
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
######## Intro ###############################################################

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

def splashscreen(screen, delaytime):

    images = [
    load_image("splashscreen_1.bmp"),
    load_image("splashscreen_2.bmp"),
    load_image("splashscreen_3.bmp"),
    load_image("splashscreen_4.bmp"),
    load_image("splashscreen_5.bmp"),
    load_image("splashscreen_6.bmp"),
    load_image("splashscreen_7.bmp"),
    load_image("splashscreen_8.bmp"),
    load_image("splashscreen_9.bmp"),
    load_image("splashscreen_10.bmp"),
    ]

    apeassound = load_sound("apeass.wav")

    counter = 0
    num = 0

    while counter < 10:
        
        background_image, background_rect = images[num]
        screen.blit(background_image, (0, 0))
        pygame.display.update()
        pygame.display.flip()

        counter = counter + 1
        num = num + 1

        pygame.time.delay(delaytime)

    num = 9
    counter = 0

    apeassound.play()
    pygame.time.delay((6000))

    while counter < 9:
        
        background_image, background_rect = images[num]
        screen.blit(background_image, (0, 0))
        pygame.display.update()
        pygame.display.flip()

        counter = counter + 1
        num = num - 1

######## Main ################################################################
############Sprites###########################################################

class settings():
    def Settings():
        self.gravity = 10
        self.atmospher = 20

def square():
    image = pygame.Surface((20, 20))
    pygame.draw.rect(image, (200, 200, 200), (0, 0, 20, 20), 0)
    return image.convert()

class Dude(pygame.sprite.Sprite):
    """This class is for the dude that moves around the screen."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            load_image("dude.bmp"),
            load_image("dude_2.bmp"),
            load_image("dude_3.bmp"),
            load_image("dude_4.bmp"),
            load_image("dude_5.bmp"),
        ]
        self.image, self.rect = load_image("dude.bmp")
        self.xvel = 0
        self.yvel = 0
        self.weight = 6
        self.health = 100
        self.anim = 0
        self.anim_max = 5

        self.rect.center = (320,450)
        self.rect.left = 200
        self.rect.top = 200

    def update(self):
        #self.rect.move_ip(((self.xvel), (self.yvel - settings.Settings.gravity*self.mass)))

        self.rect.move_ip(self.xvel, self.yvel)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 640:
            self.rect.right = 640
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 480:
            self.rect.bottom = 480
        if self.rect.bottom != 480:
            self.yvel = self.yvel
        if self.anim == self.anim_max - 1:
            self.anim = 0
        elif self.anim < self.anim_max:
            self.anim = self.anim + 1

        monkeyman = self.anim

        self.image, self.rect = self.images[monkeyman]
        
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
    splashscreen(screen, 50)
    screenfade(screen, 1)
    pygame.time.delay(30)

def main():

    intro()
    
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("BEHOLD, THE MONKEYLORD!")
    jeff = square()
    screen.blit(jeff, (30, 30))
    dude = Dude()
    dudesprite = pygame.sprite.RenderClear(dude)

    clock = pygame.time.Clock()
    running = 1

    while running == 1:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 0
                elif event.key == K_RIGHT:
                    dude.xvel = 3
                elif event.key == K_LEFT:
                    dude.xvel = -3
                elif event.key == K_SPACE:
                    dude.yvel = -12
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    dude.xvel = dude.xvel
                elif event.key == K_LEFT:
                    dude.xvel = dude.xvel
                elif event.key == K_w:
                    dude.yvel = dude.yvel
                
        screen.fill((0, 0, 0))
        dudesprite.update()
        dudesprite.draw(screen)

        pygame.display.update()
        pygame.display.flip()

        clock.tick(20)

pygame.time.delay(200)
main()

print "Done"

# Program Finished ###########################################################
#### Phew! ###################################################################
