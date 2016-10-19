class path:
	def __init__(self,strng,tcst):
		self.strng = strng
		self.tcst = tcst

def cost(pos,map):
	if pos[0]<0 or pos[0]>=len(map[0]) or pos[1]<0 or pos[1]>=len(map):
		#print pos,"off map"
		return None
	t = map[pos[1]][pos[0]]
	if (t.unit and t.unit.cost==None) or t.speed<0:
		return None
	sp = t.speed
	if t.unit and t.unit.cost:
		sp+=t.unit.cost
	return sp
	
class node:
	def __init__(self,pos,map,parent=None):
		self.pos = pos
		self.map = map
		self.parent = parent
		#print "     node:",self.pos
		self.g = self.get_g()
	def get_g(self,dbg=0):
		c = cost(self.pos,self.map)
		if c==None:
			return None
		pg = 0
		if self.parent and self.parent.parent:
			pg = self.parent.g
		if pg==None:
			return None
		c += pg
		return c
	def get_h(self,dest):
		import math
		#return math.sqrt((dest[0]-self.pos[0])**2+(dest[1]-self.pos[1])**2)
		return abs(dest[0]-self.pos[0])+abs(dest[1]-self.pos[1])
	def get_f(self,dest):
		g = self.g
		f = g+self.get_h(dest)
		return f
		
def onli(n,li):
	for cn in li:
		if cn.pos[0]==n.pos[0] and cn.pos[1]==n.pos[1]:
			return cn
	return False
	
def findpath(spos,epos,map,ignorelast=None):
	if not ignorelast and not cost(epos,map):
		return []
	open = [node(spos,map)]
	closed = []
	while open:
		#print "li:",open,closed
		def _cmp(nodea,nodeb):
			return cmp(nodea.get_f(epos),nodeb.get_f(epos))
		open.sort(_cmp)
		p = open[0]
		#print "processing",p.pos
		if p.pos[0]==epos[0] and p.pos[1]==epos[1]:
			nodes = []
			top = p
			while p.parent:
				nodes.insert(0,p)
				p = p.parent
			return nodes
		closed.append(p)
		del open[0]
		for dir in [-1,0],[1,0],[0,-1],[0,1]:
			n = node([p.pos[0]+dir[0],p.pos[1]+dir[1]],map,p)
			cn = onli(n,open)
			if n.pos[0]==epos[0] and n.pos[1]==epos[1]:
				nodes = []
				top = n
				while n.parent:
					nodes.insert(0,n)
					n = n.parent
				if ignorelast and top.parent:
					del nodes[-1]
				return nodes
			if cn:
				if cn.g<n.g:
					pass
				else:
					cn.parent = n
					cn.g = cn.get_g()
			elif not onli(n,closed) and n.g!=None:
				open.append(n)
	#print "no path found"
	return None
	
def go():
	import map
	m = map.map()
	nm = []
	for row in m.map:
		s = ""
		for col in row:
			if col.unit:
				s+="u"
			else:
				s+=col.terrain[0]
		nm.append(s)
		print s
	pth = findpath([0,0],[5,8],m.map)
	if pth:
		print [n.pos for n in pth[0]],pth[1]
	else:
		print "no path found"
		
if __name__=="__main__":
	import profile
	profile.run("go()")
	#go()