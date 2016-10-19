#==============================================================================
# resource.py
#
#
#==============================================================================

import pygame
import weakref

#==============================================================================

def load_image(filename):
	try:
		return pygame.image.load(filename).convert_alpha()
	except:
		print "Unable to load image '" + filename + "'. Filename may be wrong."
		return pygame.Surface((10,10))

def load_sound(filename):
	class NoneSound:
		def play(self):
			print "No sound!"
	if not pygame.mixer:
		return NoneSound()
	try:
		return pygame.mixer.Sound(filename)
	except:
		print "Unable to load sound '" + filename + "'. Filename may be wrong."
		return NoneSound()

#==============================================================================
# COPYPASTA!

class ResourceController(object):
	def __init__(self, loader):
		self.__dict__.update(dict(
			names = {},
			cache = weakref.WeakValueDictionary(),
			loader = loader
		))
		
	def __setattr__(self, name, value):
		self.names[name] = value
		
	def __getattr__(self, name):
		try:
			img = self.cache[name]
		except KeyError:
			img = self.loader(self.names[name])
			self.cache[name] = img
		return img
	
	def load_multi(self, name, partial_filename, type, range):
		for n in range:
			filename = partial_filename + str(n) + type
			attrname = name + str(n)
			self.__setattr__(attrname, filename)
	
	def retrieve_multi(self, names):
		imgs = []
		for name in names:
			imgs.append(self.__getattr__(name))
		return imgs
	
	def retrieve_range(self, name, range):
		imgs = []
		for n in range:
			imgs.append(self.__getattr__(name+str(n)))
		return imgs
	
class ImageController(ResourceController):
	def __init__(self):
		ResourceController.__init__(self, load_image)
class SoundController(ResourceController):
	def __init__(self):
		ResourceController.__init__(self, load_sound)