# EXPERIMENT FAILED LOL


import threading


class Window(threading.Thread):
	def run(self):
		import pygame
		from pygame.locals import *
		pygame.init()
		self.display = pygame.display.set_mode((800,600))
		while 1:
			for e in pygame.event.get():
				if e.type == QUIT:
					return
			pygame.display.update

def main():
	win1 = Window()
	win2 = Window()
	
	win1.start()
	#win2.start()

if __name__ == '__main__': main()