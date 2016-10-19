#==============================================================================
# noise.py
# Does random things.
#
#==============================================================================

from random import random
from math import sin, cos, radians

def Noise(x):
	""" Some stolen pseudo-random number function. God knows why I'm using it,
		but, alas, I do not."""
	x = (x<<13) ^ x;
	return ( 1.0 - ( (x * (x * x * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

def MakeNoisyCircle(radius, numpoints, magnitude):
	""" Makes a circle and distorts the radius at different values of theta (n). """
	
	angleperpoint = 360.0/numpoints
	points = []
	for n in range(0,numpoints):
		rand = random()
		r = (Noise(int(n*rand*10))*magnitude + radius)
		points.append((r*cos(radians(n*angleperpoint)),r*sin(radians(n*angleperpoint))))
	return points