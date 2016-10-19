import os, pygame

class Screen():
	def __init__(self,SCREENRECT,title):
		pygame.display.init()
		self.display = pygame.display.set_mode(SCREENRECT)
		pygame.display.set_caption(str(title))
	def show(self,image):
		pos = ((self.display.get_width()/2-image.get_width()/2),(self.display.get_height()/2-image.get_height()/2))
		self.display.fill((0,0,0))
		self.display.blit(image,(pos))
	def drawsprites(groups, image):
		for group in groups:
			group.draw(image)
		return image
	def destroy():
		pygame.display.quit()