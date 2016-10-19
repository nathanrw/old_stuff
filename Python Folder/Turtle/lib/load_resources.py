import pygame, os
from pygame.locals import *

def load_image(file, colorkey=False):
	file = os.path.join('data', file)
	try:
		image = pygame.image.load(file)
		colorkey = image.get_at((0, 0))
		if colorkey is True:
			image.set_colorkey(colorkey, pygame.RLEACCEL)
	except:
		print 'Unable to load: ' + file
	return image.convert_alpha()

def load_images(files, colorkey=False):
	imgs = []
	for file in files:
		imgs.append(load_image(file,colorkey))
	return imgs

def load_image_sequence(name, format, number, colorkey=False):
	imgs = []
	n = 0
	while n <= number:
		imgs.append(load_image(name+str(n)+format, colorkey))
		n += 1
	return imgs