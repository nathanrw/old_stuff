#==============================================================================
# collide_detect.py
#
# For testing of collision detection.
#==============================================================================

import pygame; from pygame.locals import *
import math

from maths import *

#==============================================================================

def minMove(a, b):
	"""
	Might be an idea to put all the others in here.
	"""
	min_move = [0,0]
	
	#
	# Do stuff
	#
	
	return min_move

def minMove_AABB_AABB(rect_a, rect_b):
	"""
	Used for handling rect collisions. Faster than
	the polygon one.
	"""
	min_move = (0,0)
	if rect_a.colliderect(rect_b):
		intersection = rect_a.clip(rect_b)
		
		dist_y = intersection.bottom - intersection.top
		dist_x = intersection.right - intersection.left
		
		if mod(dist_y) > mod(dist_x):
			if intersection.right > rect_b.center[0]:
				dist_x = -dist_x
			min_move = (dist_x,0)
		elif mod(dist_x) > mod(dist_y):
			if intersection.top > rect_b.center[1]:
				dist_y = -dist_y
			min_move = (0, dist_y)
			
	return min_move

def minMove_Polygon_Polygon(poly_a, poly_b):
	"""
	Handles collisions between convex polygons. Currently
	that means units hitting ramps.
	
	Possibly needs to be sped up.
	
	Could be sped up by storing the polygon centres.
	"""
	edges = getEdges(poly_a) + getEdges(poly_b)
	min_move = 9999 # Like infinity but smaller :P
	min_axis = (0,0)
	for edge in edges:
		e = Sub2DVector(edge[1],edge[0])
		axis = Unit2DVector((-e[1],e[0]))
		
		min_a, max_a = projectPolygon(axis, poly_a)
		min_b, max_b = projectPolygon(axis, poly_b)
		
		overlap = overlapProjections(min_a,max_a,min_b,max_b)
		if overlap > 0:
			return (0,0)
		
		overlap = mod(overlap) + 0.1
		
		if overlap < min_move:
			min_move = overlap
			min_axis = axis
		
	diff = Sub2DVector(getCentre(poly_a),getCentre(poly_b))
	if DotProduct2DVector(diff,min_axis) < 0:
		min_axis = Sub2DVector((0,0),min_axis)
		
	return ScalMul2DVector(min_axis,min_move)

def minMove_AABB_Polygon(rect, poly):
	rect_poly = getPolyFromRect(rect)
	minMove =  minMove_Polygon_Polygon(rect_poly, poly)
	return (-minMove[0],-minMove[1])

#==============================================================================

def main():
	
	pygame.init()
	screen = pygame.display.set_mode((800,600))
	
	a = Polygon2D()
	s = 1.0
	a.add(Vector2D(-50*s,-50*s))
	#a.add(Vector2D(50*s,-50*s))
	a.add(Vector2D(50*s,50*s))
	a.add(Vector2D(-50*s,50*s))
	
	a.setPosition(Vector2D(400,300))
	
	b = Polygon2D()
	s = 5
	b.add(Vector2D(-50*s,-50*s))
	b.add(Vector2D(50*s,-50*s))
	b.add(Vector2D(50*s,50*s))
	b.add(Vector2D(-50*s,50*s))
	
	c = pygame.Rect(0,0,100,100)
	c.center = (800,250)
	
	v = Vector2D(-1,0)
	
	while 1:
		for e in pygame.event.get():
			if e.type == QUIT:
				pygame.quit()
				return
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					pygame.quit()
					return
		b.setPosition(Vector2D(pygame.mouse.get_pos()))
		minMove = minMove_Polygon_Polygon(a.getPoints(), b.getPoints())
		b.move(-Vector2D(minMove))
		pygame.mouse.set_pos(b.getPosition())
		
		c.x += v.x
		c.y += v.y
		minMove = Vector2D(minMove_AABB_Polygon(c, a.getPoints()))
		c.x -= minMove.x
		c.y -= minMove.y
		v.x -= minMove.x
		v.y -= minMove.y
		
		screen.fill((0,0,0))
		pygame.draw.lines(screen, (255,100,100), 1, a.getPoints(), 4)
		pygame.draw.lines(screen, (100,100,255), 1, b.getPoints(), 2)
		pygame.draw.rect(screen,(100,255,0),c,1)
		pygame.display.update()

if __name__ == '__main__': main()