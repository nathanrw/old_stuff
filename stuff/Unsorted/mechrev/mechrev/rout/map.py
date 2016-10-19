import pygame
import random
import units

si = 32

def gs(col):
	"""Make tile that's that color"""
	s = pygame.Surface([si,si])
	s.fill(col)
	return s
tpic = pygame.image.load("gfx/tile.png")
gspic = tpic.subsurface([[0,0],[32,32]])
wtpic = tpic.subsurface([[32,0],[32,32]])
fspic = tpic.subsurface([[64,0],[32,32]])
mtpic = tpic.subsurface([[96,0],[32,32]])
brpic = tpic.subsurface([[128,0],[32,32]])
brbrpic = tpic.subsurface([[160,0],[32,32]])
flrpic = tpic.subsurface([[192,0],[32,32]])
wlpic = tpic.subsurface([[224,0],[32,32]])
crtpic = tpic.subsurface([[256,0],[32,32]])
twpic = tpic.subsurface([[288,0],[32,32]])

gdata = {"grass":gspic,"mountain":mtpic,"water":wtpic,"forest":fspic,"bridge":brpic,"brokenbridge":brbrpic,
	"floor":flrpic,"wall":wlpic,"crates":crtpic,"town":twpic}
spdata = {"grass":1,"mountain":3,"water":-1,"forest":2,"bridge":1,"brokenbridge":None,
	"floor":1,"wall":None,"crates":2,"town":2}

class tile:
	def __init__(self,terrain,pos):
		self.terrain = terrain
		self.unit = None
		self.playerstart = False
		self.pos = pos
	def __setattr__(self,arg,var):
		self.__dict__[arg]=var
		if arg=="terrain":
			self.surf = gdata[self.terrain]
			self.speed = spdata[self.terrain]

class map:
	si = si
	def __init__(self,file="",lines=None):
		map = []
		if file:
			try:
				f = open(file)
			except:
				file=""
		mp = None
		if lines:
			mp = lines
		elif file:
			l = f.readlines()
			mp = eval(l[0])
		if mp:
			for y in range(480/si):
				row = []
				for x in range(640/si):
					ti = mp[y][x]
					nt = tile(ti[0],[x,y])
					if len(ti)>1:
						if ti[1]=="playerstart":
							nt.playerstart = True
						else:
							nt.unit = units.unit(ti[1],self,[x,y])
					row.append(nt)
				map.append(row)
			if file:
				f.close()
		if not mp:
			for y in range(480/si):
				row = []
				for x in range(640/si):
					nt = tile(random.choice(["mountain","mountain","grass","grass","grass","grass","grass","grass","water","forest"]),[x,y])
					row.append(nt)
					if nt.terrain == "grass":
						if random.randint(0,15)==0:
							nt.unit = units.unit("robot",self,[x,y])
				map.append(row)
		self.map = map
	def clearunit(self,u):
		self.map[u.pos[1]][u.pos[0]].unit=None
	def gettile(self,pos):
		if pos[0]<0 or pos[1]<0 or pos[0]>=len(self.map[0]) or pos[1]>=len(self.map):
			return None
		return self.map[pos[1]][pos[0]]
	def getunits(self):
		units=[]
		for y in range(len(self.map)):
			for x in range(len(self.map[0])):
				u = self.map[y][x].unit
				if u:
					units.append(u)
		return units
	def getplayerstarts(self):
		units=[]
		for y in range(len(self.map)):
			for x in range(len(self.map[0])):
				u = self.map[y][x].playerstart
				if u:
					units.append(u)
		return units
	def display(self,surf=None):
		if not surf:
			surf = pygame.display.get_surface()
		y=0
		for row in self.map:
			x=0
			for col in row:
				surf.blit(col.surf,[x,y])
				x+=si
			y+=si
	def tostr(self):
		mp = []
		for y in range(480/si):
			row = []
			for x in range(640/si):
				ti = self.map[y][x]
				newti = []
				newti.append(ti.terrain)
				if ti.unit:
					newti.append(ti.unit.type)
				elif ti.playerstart:
					newti.append("playerstart")
				row.append(newti)
			mp.append(row)
		return mp
	def save(self,file):
		f = open(file,"w")
		f.write(repr(mp))
		f.close()
	
		
	
