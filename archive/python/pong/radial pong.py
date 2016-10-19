#==============================================================================
# Radial Pong
#==============================================================================

#==============================================================================
# Imports
#==============================================================================

import pygame
from pygame.locals import *
from math import sin, cos, pi, sqrt, atan
from random import random as rnd

#==============================================================================
# Constants
#==============================================================================

TwoPi = 2*pi

#==============================================================================
# Subroutines
#==============================================================================

def draw_arc(surface, colour, position, radius, theta, alpha, width=1):
	""" surface: Surface to draw the arc onto,
		radius : Take a wild guess.
		theta  : Angle of arc. Angle between first and second radii is theta.
		alpha  : Angle from vertical from which to start drawing. Angle between
				vertical and second radius is alpha.
		Draws an arc of a circle.
	"""
	locked = surface.get_locked()
	if not locked:
		surface.lock()
	step = 1.0/radius
	angle = alpha
	lim = alpha + theta
	while angle < lim:
		x = radius * sin(angle) + position[0]
		y = radius * cos(angle) + position[1]
		pygame.draw.rect(surface, colour, Rect(x,y,width,width))
		angle += step
	if not locked:
		surface.unlock()

def draw_circle(surface, colour, position, radius, width=1):
	draw_arc(surface,colour,position,radius,TwoPi,0.0,width)

def rndcol():
	return (100+rnd()*155,100+rnd()*155,100+rnd()*155)
def rndsign():
	r = rnd()
	return (r>=0.5)-(r<0.5)
def checksign(n):
	return (n>0)-(n<0)
def checkpair(x,y):
	return (checksign(x),checksign(y))

#==============================================================================
# Globals
#==============================================================================

pygame.init()

# Colours =====================================================================
BACK = (40,40,40)
MID  = (0,0,0)
FORE = (240,240,240)

# Display =====================================================================
screen = pygame.display.set_mode((800,600))

# Game ========================================================================
numplayers = 3
playerarclength = pi/numplayers
batarclength = playerarclength/3

step = TwoPi/numplayers
angles = []
bats = []
walls = []

for x in range(0, numplayers):
	angles.append(x * step + playerarclength/2)
	bats.append([x * step + playerarclength - batarclength / 2, rndcol() , 0, 0])
	wl = x * step - playerarclength/2
	if wl < 0:
		wl = TwoPi + wl
	walls.append(wl)

ballr = 0
balltheta = 3*pi/2

r = lambda r: (r>=0.5)-(r<0.5)

ballvelx = rnd()*20*r(rnd())
ballvely = rnd()*20*r(rnd())
#==============================================================================
# Game
#==============================================================================

def draw_arena():
	screen.fill(BACK)
	w = screen.get_width()
	h = screen.get_height()
	r = h/2 - 20
	for wl in walls:
		draw_arc(screen, FORE, (w/2, h/2), r, playerarclength, wl, 2)
	for a in angles:
		draw_arc(screen, MID, (w/2, h/2), r, playerarclength, a, 2)
	for b in bats:
		draw_arc(screen, b[1], (w/2, h/2), r-10, batarclength, b[0]+b[2], 2)
	pygame.draw.circle(screen, (255,255,255), (int(ballr*sin(balltheta)+w/2),int(ballr*cos(balltheta)+h/2)), 3)

def get_input():
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			return 0
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				return 0
			
			elif event.key == K_w:
				if numplayers > 0:bats[0][3] = 1
			elif event.key == K_e:
				if numplayers > 0: bats[0][3] = -1
			elif event.key == K_r:
				if numplayers > 1: bats[1][3] = 1
			elif event.key == K_t:
				if numplayers > 1: bats[1][3] = -1
			elif event.key == K_y:
				if numplayers > 2: bats[2][3] = 1
			elif event.key == K_u:
				if numplayers > 2: bats[2][3] = -1
			elif event.key == K_i:
				if numplayers > 3: bats[3][3] = 1
			elif event.key == K_o:
				if numplayers > 3: bats[3][3] = -1
				
		elif event.type == KEYUP:
			if event.key == K_w:
				if numplayers > 0:bats[0][3] = 0
			elif event.key == K_e:
				if numplayers > 0: bats[0][3] = 0
			elif event.key == K_r:
				if numplayers > 1: bats[1][3] = 0
			elif event.key == K_t:
				if numplayers > 1: bats[1][3] = 0
			elif event.key == K_y:
				if numplayers > 2: bats[2][3] = 0
			elif event.key == K_u:
				if numplayers > 2: bats[2][3] = 0
			elif event.key == K_i:
				if numplayers > 3: bats[3][3] = 0
			elif event.key == K_o:
				if numplayers > 3: bats[3][3] = 0
	
	return 1

def ballbounce():
	global ballr, balltheta, ballvelx, ballvely
	ballr -= 4
	ballvelx = -ballvelx+rndsign()*rnd()*2
	ballvely = -ballvely+rndsign()*rnd()*2

def update_ball():
	global ballr, balltheta, ballvelx, ballvely
	
	# Polar --> Regular coordinates
	x = ballr * sin(balltheta)
	y = ballr * cos(balltheta)
	
	# Move
	x += ballvelx
	y += ballvely
	
	# Regular --> Polar coordinates
	r = sqrt(x**2+y**2)
	
	theta = atan(x/(y+0.00000000001))
	
	signs = checkpair(x,y)
	if signs == (-1,1):
		theta = TwoPi + theta
	elif signs == (-1,-1):
		theta = pi + theta
	elif signs == (1,-1):
		theta = pi + theta
		
	balltheta = theta
	ballr = r
	
	# Collision detection
	
	for wl in walls:
		if ( ballr > screen.get_height()/2 - 23 ) :
			ballbounce()
			
	for bt in bats:
		if ( ballr > screen.get_height()/2 - 35 ) \
		and ( bt[0]+bt[2] < balltheta < bt[0]+batarclength+bt[2] ) :
			ballbounce()
			
	for an in angles:
		if ( ballr > screen.get_height()/2 - 26 ) \
		and ( an < balltheta < an+playerarclength ) :
			ballr = 0
			ballvelx = rnd()*20*rndsign()
			ballvely = rnd()*20*rndsign()
			
def update_bats():
	for bat in bats:
		bat[2] -= (checksign(bat[3])) * (pi/180)
		if bat[2] > playerarclength/4:
			bat[2] = playerarclength/4
		elif bat[2] < -playerarclength/4:
			bat[2] = -playerarclength/4
			
def update():
	update_bats()
	update_ball()
	draw_arena()
	pygame.display.update()

def mainloop():
	while 1:
		if not get_input():
			return
		update()

#==============================================================================
# Main
#==============================================================================

def main():
	mainloop()

if __name__ == '__main__': main()
