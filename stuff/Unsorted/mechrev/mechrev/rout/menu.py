import pygame
import pygame.font
pygame.font.init()

def strt():
	print "start!"

class menu:
	def __init__(self,options=["start","quit","continue","laugh","blah","hahahaha","position unit"],pos=[100,100],funcs={"start":strt}):
		self.optionrenders = []
		fnt = pygame.font.SysFont("Verdana",14)
		self.width = 0
		self.height = 0
		for o in options:
			s = fnt.render(o,1,[255,255,255])
			wi,hi = s.get_size()
			if wi+4>self.width:
				self.width=wi+4
			self.height+= hi+4
			self.optionrenders.append(s)
		self.back = pygame.Surface([self.width,self.height])
		self.back.fill([0,0,255])
		self.back.set_alpha(200)
		self.sel = pygame.Surface([self.width,self.optionrenders[0].get_size()[1]+4])
		self.sel.fill([0,0,255])
		self.sel.set_alpha(220)
		self.pos = list(pos)
		self.options = options
		self.funcs = funcs
		self.o=0
	def display(self,surf=None):
		if self.pos[1]+self.height>480:
			self.pos[1] = 480-self.height
		if self.pos[0]+self.width>640:
			self.pos[0]=640-self.width
		if self.pos[0]<0:
			self.pos[0] = 0
		if self.pos[1]<0:
			self.pos[1] = 0
		if not surf:
			surf = pygame.display.get_surface()
		bck = self.back.convert()
		x=2
		y=0
		for o in self.optionrenders:
			bck.blit(o,[x,y+2])
			y+=o.get_size()[1]+4
		surf.blit(bck,self.pos)
		if self.o>=0:
			surf.blit(self.sel,[self.pos[0],self.pos[1]+self.o*(self.optionrenders[self.o].get_size()[1]+4)])
			surf.blit(self.optionrenders[self.o],[self.pos[0]+2,self.pos[1]+self.o*(self.optionrenders[self.o].get_size()[1]+4)+2])
