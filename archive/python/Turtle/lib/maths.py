#==============================================================================
# maths.py
# Equals sign, equals sign, equals all the way.
#
# Some maths I kept having to write out.
#
# There's currently so much redundant crap in here that it needs a rather
# large amount of stripping down.
#
#==============================================================================

from math import sin, cos, sqrt, pi, pow, hypot
import operator
# Some constants

piby180 = pi/180
twopi = pi*2

#==============================================================================
# 2D Vector maths
#==============================================================================

class Vector2D(object):
	__slots__ = ['x', 'y']

	def __init__(self,x,y=None):
		if y == None:
			self.x = float(x[0])
			self.y = float(x[1])
		else:
			self.x = float(x)
			self.y = float(y)

	def __len__(self):
		return 2

	def __getitem__(self,index):
		if index == 0:
			return self.x
		elif index == 1:
			return self.y
		else:
			print "Index out of bounds."

	def __setitem__(self,index,value):
		if index == 0:
			self.x = value
		elif index == 1:
			self.y = value
		else:
			print "Index out of bounds."

	def __getstate__(self):
		return [self.x,self.y]

	def __repr__(self):
		return "Vector2D<"+ str((self.x,self.y))+">"

	def __neg__(self):
		return Vector2D(-self.x,-self.y)

	def __add__(self,b):
		if isinstance(b,Vector2D):
			return Vector2D(self.x+b.x,self.y+b.y)
		else:
			return Vector2D(self.x+b,self.y+b)

	def __sub__(self,b):
		if isinstance(b,Vector2D):
			return Vector2D(self.x-b.x,self.y-b.y)
		else:
			return Vector2D(self.x-b,self.y-b)

	def __mod__(self,b):
		if isinstance(b,Vector2D):
			pass
		else:
			print "Cross product failed"
	
	def __div__(self,b):
		return Vector2D(self.x/b,self.y/b)
	
	def __mul__(self,b):
		if isinstance(b,Vector2D):
			return self.x*b.x+self.y*b.y
		else:
			return Vector2D(self.x*b,self.y*b)

	def magnitude(self):
		return hypot(self.x,self.y)

	def normalise(self):
		m = self.magnitude()
		return Vector2D(self.x/m,self.y/m)
	
	def rotate(self, angle, origin=(0,0)):
		sinval = sin(angle)
		cosval = cos(angle)
		A = self.x-origin[0]
		B = self.y-origin[1]
		return Vector2D(A*cosval - B*sinval + origin[0],A*sinval + B*cosval + origin[1])
	
	def dotProduct(self, v):
		return self.x*v.x + self.y*v.y
	
	def toTuple(self):
		return (self.x, self.y)

class Polygon2D():
	def __init__(self):
		self.points = []
		self.position = Vector2D(0,0)

	def getEdges(self):
		edges = []
		index = 0
		num_points = len(self.points)
		while index < num_points:
			edges.append((self.points[index-1], self.points[index]))
			index += 1
		return edges
	
	def getPoints(self):
		points = []
		for point in self.points:
			points.append(point + self.position)
		return points
	
	def getTuples(self):
		points = []
		for point in self.points:
			points.append((point+self.position).toTuple())
		return points
	
	def getCentre(self):
		x = 0
		y = 0
		n = 0
		points = self.getPoints()
		for point in points:
			x += point[0]
			y += point[1]
			n += 1.0
		x = x/n
		y = y/n
		return Vector2D(x, y)
	
	def move(self, vector):
		self.position = self.position + vector
		
	def setPosition(self, vector):
		self.position = vector
	
	def getPosition(self):
		return self.position
	
	def add(self, point):
		self.points.append(point)

def Add2DVector(a,b):
	return [a[0]+b[0],a[1]+b[1]]

def Sub2DVector(a,b):
	return [a[0]-b[0],a[1]-b[1]]

def Mul2DVector(a,b):
	return [a[0]*b[0],a[1]*b[1]]

def ScalMul2DVector(a,n):
	return [a[0]*n,a[1]*n]

def DotProduct2DVector(a, b):
	return a[0]*b[0] + a[1]*b[1]

def Rotate2DVector(vec, angle, origin=[0,0]):
	
	sinval = sin(angle)
	cosval = cos(angle)
	
	A = vec[0]-origin[0]
	B = vec[1]-origin[1]
	
	return [A*cosval - B*sinval + origin[0], A*sinval + B*cosval + origin[1]]

def Magnitude2DVector(vec):
	return hypot(vec[0],vec[1])

def Unit2DVector(vec):
	m = 1.0/Magnitude2DVector(vec)
	return [m*vec[0],m*vec[1]]

def Distance2DPoints2D(a,b):
	return Sub2DVector(a,b)

def Distance1DPoints2D(a,b):
	return Magnitude2DVector(Sub2DVector(a,b))

def Centre2DVectors(a, b):
	x = (a[0] + b[0])/2
	y = (a[1] + b[1])/2
	return x, y

def projectPolygon(axis, polygon):
	count = 0
	num = len(polygon)
	dotproduct = DotProduct2DVector(axis,polygon[0])
	min = dotproduct
	max = dotproduct
	while count < num:
		dotproduct = DotProduct2DVector(axis, polygon[count])
		if dotproduct < min: min = dotproduct
		elif dotproduct > max: max = dotproduct
		count += 1
	return min, max

def overlapProjections(min_a, max_a, min_b, max_b):
	if min_a < min_b:
		return  (min_b - max_a)
	else:
		return  (min_a - max_b)

def getEdges(polygon):
	edges = []
	index = 0
	num_points = len(polygon)
	while index < num_points:
		edges.append((polygon[index-1], polygon[index]))
		index += 1
	return edges

def getCentre(polygon):
	x = 0
	y = 0
	n = 0
	for point in polygon:
		x += point[0]
		y += point[1]
		n += 1.0
	x = x/n
	y = y/n
	return [x,y]

#==============================================================================
# 3D Vector Maths
#==============================================================================

class Vector3D(object):
	__slots__ = ['x', 'y', 'z']

	def __init__(self,x,y=None,z=None):
		if y == None:
			self.x = float(x[0])
			self.y = float(x[1])
			self.z = float(x[2])
		else:
			self.x = float(x)
			self.y = float(y)
			self.z = float(z)

	def __len__(self):
		return 3

	def __getitem__(self,index):
		if index == 0:
			return self.x
		elif index == 1:
			return self.y
		elif index == 2:
			return self.z
		else:
			print "Index out of bounds."

	def __setitem__(self,index,value):
		if index == 0:
			self.x = value
		elif index == 1:
			self.y = value
		elif index == 2:
			self.z = value
		else:
			print "Index out of bounds."

	def __getstate__(self):
		return [self.x,self.y,self.z]

	def __repr__(self):
		return "Vector3D"+ str((self.x,self.y,self.z))

	def __neg__(self):
		return Vector3D(-self.x,-self.y,-self.z)

	def __add__(self,b):
		if isinstance(b,Vector3D):
			return Vector3D(self.x+b.x,self.y+b.y,self.z+b.z)
		else:
			return Vector3D(self.x+b,self.y+b,self.z+b)

	def __sub__(self,b):
		return self + (-b)

	def __mod__(self,b):
		if isinstance(b,Vector3D):
			return Vector3D(self.y*b.z-self.z*b.y,
							self.x*b.z-self.z*b.x,
							self.x*b.y-self.y*b.x)
		else:
			print "Cross product failed"
			
	def __mul__(self,b):
		if isinstance(b,Vector3D):
			return self.x*b.x+self.y*b.y+self.z*b.z
		else:
			return Vector3D(self.x*b,self.y*b,self.z*b)
	
	def __div__(self,b):
		return Vector3D(self.x/b,self.y/b,self.z/b)

	def mag(self):
		return math.sqrt(self.x**2+self.y**2+self.z**2)

	def unit(self):
		m = 1/self.mag()
		return Vector3D(self.x*m,self.y*m,self.z*m)

def Add3DVector(a,b):
	return [ a[0]+b[0], a[1]+b[1], a[2]+b[2] ]

def Sub3DVector(a,b):
	return [ a[0]-b[0], a[1]-b[1], a[2]-b[2] ]

def CrossProduct3DVector(a,b):
	return [ a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0] ]

def DotProduct3DVector(a,b):
	return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def Mul3DVector(a,x):
	return [a[0]*x, a[1]*x, a[2]*x]

def Rotate3DVector(a, angles, origin=[0,0,0]):
	a = Sub3DVector(a, origin)
	Y, Z = Rotate2DVector([a[1], a[2]], angles[0])
	X, Z = Rotate2DVector([a[0],  Z  ], angles[1])
	X, Y = Rotate2DVector([ X   , Y  ], angles[2])
	return Add3DVector([X,Y,Z], origin)

def Magnitude3DVector(a):
	if a[0] == 0 and a[1] == 0: return 0
	return sqrt(a[0]**2+a[1]**2+a[2]**2)

def Unit3DVector(a):
	if a[0] == 0 and a[1] == 0: return [0,0]
	m = 1.0/Magnitude3DVector(a)
	return [a[0]*m,a[1]*m,a[2]*m]

def Distance3D_1D(a,b):
	return Magnitude3DVector(Sub3DVector(a,b))

#==============================================================================

def Project3DTo2D(a, surface, dist, screenx=0, screeny=0):
	c = dist/(a[2]+0.00001)
	return a[0]*c+screenx, a[1]*c+screeny

def Project2DTo1D(a, dist, screenxovertwo):
	return int(a[0]*dist/(a[1]+0.00001) + screenxovertwo)

#==============================================================================

def mod(x):
	if x < 0:
		return -x
	else: return x

def getPolyFromRect(rect):
	A = (rect.x,rect.y+rect.h)
	B = (rect.x+rect.w,rect.y+rect.h)
	C = (rect.x+rect.w,rect.y)
	D = (rect.x,rect.y)
	return (A,B,C,D)

#==============================================================================

class Matrix(object):
	def __init__(self, rows):
		self.rows = rows
	
	def __len__(self):
		return len(self.rows[0])
	
	def __getitem__(self, index):
		return self.rows[index]
	
	def __getstate__(self):
		print "Getstate lol"
		return 0
	
	def __repr__(self):
		string = ""
		for row in self.rows:
			string += "[ "
			for item in row:
				string += str(item) + ", "
			string = string[:-2]
			string += " ]\n"
		return string
	
	def __neg__(self):
		new_rows = []
		for row in self.rows:
			new_row = []
			for item in row:
				new_row.append(-item)
			new_rows.append(new_row)
		return Matrix(new_rows)
	
	def __add__(self, b):
		try:
			x=b[0]
		except:
			return Matrix( map( lambda row: \
			map( lambda item: item + b, row), self.rows))
			
		if not (len(self.rows) == len(b.rows) and \
		len(self.rows[0]) == len(b.rows[0])):
			print "fail"; return
		
		row_counter = 0
		item_counter = 0
		new_rows = []
		
		while row_counter < len(self.rows):
			new_row = []
			
			while item_counter < len(self.rows[0]):
				new_row.append(self.rows[row_counter][item_counter] + \
				b.rows[row_counter][item_counter])
				
			new_rows.append(new_row)
			
		return Matrix(new_rows)
	
	def __sub__(self, b):
		return self + -b
	
	def __mul__(self, matrix):
		if len(self.rows) != len(matrix.rows[0]):
			print "fail"
			return
		
		row_counter = 0
		row_item_counter = 0
		column_item_counter = 0
		new_matrix = []
		
		while row_counter < len(self.rows):
			row_item_counter = 0
			new_row = []
			
			while row_item_counter < len(self.rows[0])-1:
				column_item_counter = 0
				new_row_item = 0
				
				while column_item_counter < len(matrix.rows):
					new_row_item += self.rows[row_counter][column_item_counter] * \
					matrix.rows[column_item_counter][row_item_counter]
					column_item_counter += 1
					
				new_row.append(new_row_item)
				row_item_counter += 1
				
			new_matrix.append(new_row)
			row_counter += 1
			
		return Matrix(new_matrix)
	
def TranslationMatrix3D(x,y,z):
	pass
def RotationMatrix3D(a,b,c):
	pass
def ScalingMatrix3D(x,y,z):
	pass