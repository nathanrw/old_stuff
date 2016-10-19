import os, pygame
from pygame.locals import *

def MakeText(text, fontsize, colour):
    outtext = text
    font = pygame.font.Font(None, fontsize)
    text = font.render(outtext, 1, colour)
    return text

def ImportImg(name, colorkey=None):
    ULTRApath = os.path.join('data', name)
    print ULTRApath
    try:
        image = pygame.image.load(ULTRApath)
    except pygame.error, message:
        print 'Cannot load image'
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def ImportPNG(name):
    ULTRApath = os.path.join('data', name)
    print ULTRApath
    try:
        image = pygame.image.load(ULTRApath)
    except pygame.error, message:
        print 'Cannot load image'
        raise SystemExit, message
    image = image.convert_alpha()
    return image

def ImportImages(name, numimages, colorkey=None):
    Images = []
    counter = 0
    while counter <= numimages:
        fullname = name + "_" + str(counter) + ".png"
        if colorkey is None or colorkey is -1:
            try:
                Images.append(ImportImg(fullname, colorkey))
            except:
                print"Error"
                return Images
        elif colorkey is 1:
            try:
                Images.append(ImportPNG(fullname))
            except:
                print "Error"
                return Images
            
        counter += 1

    return Images

def LoadSound(name):
    class NoneSound:
	    def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
	    return NoneSound()
    fullname = os.path.join('data', name)
    print fullname
    try:
	    sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
	    print 'Cannot load sound:', fullname
	    raise SystemExit, message
    sound.set_volume(0.4)
    return sound
