from math import hypot

def add2D(a,b):
	return [a[0]+b[0],a[1]+b[1]]

def sub2D(a,b):
	return [a[0]-b[0],a[1]-b[1]]

def scale2D(a,n):
	return [a[0]*n,a[1]*n]

def distance2D(vec):
	return hypot(vec[0],vec[1])

def normalise2D(vec):
	m = 1.0/distance2D(vec)
	return [m*vec[0],m*vec[1]]