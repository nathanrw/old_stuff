class A:
	
	x = 1
	y = 2
	
	def __init__(self):
		pass
	
	def getn(self):
		return self.x
	def setn(self, val):
		self.x = val
	
	n = property(fget=getn,fset=setn)

class B(A):
	def __init__(self):
		A.__init__(self)
	
	def getn(self):
		return self.y

a = A()
b = B()

print a.n
print b.n