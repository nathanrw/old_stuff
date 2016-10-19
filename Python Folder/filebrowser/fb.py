import pygame
from pygame.locals import *

from spg import gui
from spg.gui import *
from spg import defaultStyle

import os
import sys

class FileBrowser(object):
	
	size = (400,300)
	initialised = 0
	
	def __init__(self, desktop):
		self.desktop = desktop
		self.__returnValue = None
	
	def __call__(self, dir="."):
		
		if self.initialised: return
		else: self.initialised = 1
		
		self.win = Window(size = self.size, parent = self.desktop, text = "File Browser")
		
		self.win.ALLOW_SCALE = 1
		
		def onWinClose(window):
			self.initialised = 0
		
		self.win.onClose = onWinClose
		
		self.__path = os.path.abspath(dir)
		
		self.backstack = []
		self.forwardstack = []
		
		self.txt_path = TextBox(position = (10, 60), size = (self.win.size[0]-20, 0), text = self.path, parent = self.win)
		
		self.lst_folderview = ListBox(position = (10, 80), size = (self.win.size[0]-20, self.win.size[1]-120),parent = self.win, items = [])
		self.lst_folderview.items = os.listdir(self.path)
		
		def onItemSelected(listbox):
			if listbox.selectedIndex >= len(listbox.items): return
			item = listbox.items[listbox.selectedIndex]
			path = os.path.join(self.path, item)
			self.txt_path.text = path
		
		self.lst_folderview.onItemSelected = onItemSelected
		
		self.btn_back = Button(position = (10, 35), size = (30,0), text = "<", parent = self.win)
		self.btn_back.onClick = lambda button: self.back()
		
		self.btn_up = Button(position = (45, 35), size = (30,0), text = "^", parent = self.win)
		self.btn_up.onClick = lambda button: self.up()
		
		self.btn_forward = Button(position = (80, 35), size = (30,0), text = ">", parent = self.win)
		self.btn_forward.onClick = lambda button: self.forward()
		
		self.btn_cancel = Button(position = (self.size[0]-180,self.size[1]-30), size = (80,0), text = "Cancel", parent = self.win)
		self.btn_cancel.onClick = lambda button: self.win.close()
		
		self.btn_open = Button(position = (self.size[0]-90,self.size[1]-30), size = (80, 0), text = "Open", parent = self.win)
		
		def onWinScale(w):
			self.lst_folderview.size = (w.size[0]-20, w.size[1]-120)
			self.btn_cancel.position = (w.size[0]-180,w.size[1]-30)
			self.btn_open.position = (w.size[0]-90, w.size[1]-30)
			self.txt_path.size = (w.size[0]-20, 0)
		
		self.win.onScale = onWinScale
		
		def openOnClick(button):
			path = self.txt_path.text
			if os.path.isdir(path):
				self.navigate(path)
			elif os.path.isfile(path):
				self.returnValue = path
				self.win.close()
			else:
				pass
		
		self.btn_open.onClick = openOnClick
	
	def forward(self):
		if len(self.forwardstack):
			self.backstack.append(self.path)
			self.path = self.forwardstack.pop()
	
	def back(self):
		if len(self.backstack):
			self.forwardstack.append(self.path)
			self.path = self.backstack.pop()
	
	def navigate(self, path):
		self.forwardstack = []
		self.backstack.append(self.path)
		self.path = path
	
	def up(self):
		self.navigate(os.path.split(self.path)[0])
	
	def setPath(self, path):
		self.__path = path
		self.txt_path.text = self.path
		items = os.listdir(self.path)
		self.lst_folderview.items = items
	def getPath(self):
		return self.__path
	
	path = property(fget=getPath, fset=setPath)
	
	def setVal(self, val):
		self.__returnValue = val
	def getVal(self):
		if self.__returnValue:
			rv = self.__returnValue
			self.__returnValue = None
			return rv
		return None
	
	returnValue = property(fset=setVal, fget=getVal)

def main():
	pygame.init()
	display = pygame.display.set_mode((800,600))
	defaultStyle.init(gui)
	
	desktop = Desktop()
	
	fb = FileBrowser(desktop)
	fb()
	
	while 1:
		for e in gui.setEvents():
			if e.type == QUIT:
				sys.exit()
			if e.type == KEYDOWN and e.key == K_q:
				fb()
		rv = fb.returnValue
		if rv:
			win = Window(size = (600,400), parent=desktop, text = "File Reader")
			win.ALLOW_SCALE = 1
			fl = open(rv, "r")
			lb = ListBox(position = (20, 40), parent = win, size = (win.size[0]-40,win.size[1]-60), items = [])
			def onScale(w):
				lb.size = (w.size[0]-40,w.size[1]-60)
			win.onScale = onScale
			for line in fl:
				line = line.replace("""	""","     ")
				line = line.replace("\n", "")
				lb.items.append(line)
			fl.close()
		desktop.update()
		display.fill((50,50,50))
		desktop.draw()
		pygame.display.update()

if __name__ == '__main__': main()