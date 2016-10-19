import math
import pygame
from pygame.locals import *
from vec2d import vec2d as v2d

def lerp(y1, y2, fraction):
	return y1 * (1.0 - fraction) + y2 * fraction

def cerp(y1, y2, fraction):
	angle = fraction * math.pi
	sample = (1.0 - math.cos(angle)) * 0.5
	return y1 * (1.0 - sample) + y2 * sample

interpolate = lerp

ANIM_MODE_LINEAR = 0
ANIM_MODE_COSINE = 1

def ANIM_Set_Interpolate_Mode(mode):
	global interpolate
	if mode == 0:
		interpolate = lerp
	if mode == 1:
		interpolate = cerp

def plot(surf, p1, p2, detail):
	
	l = (p2[0]-p1[0])
	xstep = l/float(detail)
	x = 0
	
	prevpoint = p1
	
	for n in xrange(0, detail):
		
		x += xstep
		fraction = x/l
		y = interpolate(p1[1], p2[1], fraction)
		
		pygame.draw.line(surf, (255,255,255), prevpoint, (p1[0]+x,y), 2)
		
		prevpoint = (p1[0]+x, y)
		
	pygame.draw.line(surf, (255,255,255), prevpoint, p2)

def plotlist(surf, points, detail):
	
	for n in xrange(len(points)-1):
		plot(surf, points[n], points[n+1], detail)

def framesFromKeyframes(keyframes, detail):
	
	ANIM_Set_Interpolate_Mode(ANIM_MODE_COSINE)
	
	framecounter = 1
	end = len(keyframes)-1
	step = 1.0/detail
	frames = []
	
	while framecounter < end:
		
		fraction = step
		subframes = []
		a = keyframes[framecounter]
		b = keyframes[framecounter+1]
		
		frames.append(a)
		
		while fraction < 1.0:
			
			subframes.append(a.interpolate(b, fraction))
			fraction += step
		
		frames.extend(subframes)
		frames.append(b)
	
	return frames

class Animation():
	
	def __init__(self, frames, framerate):
		
		self.frames = frames
		self.framerate = framerate
		
		self.frametime = 1.0/framerate
		self.length_t = len(self.frames) * self.frametime
		self.length_frames = len(self.frames)
		
		self.t = 0
		self.framecounter = 0
		self.frame = self.frames[0]
	
	def update(self, dt):
		
		self.t += dt
		
		fraction, n = math.modf(self.t*self.framerate)
		
		if n:
			
			self.framecounter += n
			
			if self.framecounter >= self.length_frames:
				
				self.framecounter -= self.length_frames
			
			if fraction:
				self.t -= (n * self.framtime + fraction)
				self.frame = self.frames[self.framecounter].interpolate(self.frames[self.framecounter+1], fraction)
				
			else:
				self.t -= n * self.frametime
				self.frame = self.frames[self.framecounter]
	
	def draw(self, surf, pos):
		
		self.frame.draw(surf, pos)
	
class Frame():
	
	def __init__(self, shapes):
		
		self.shapes = shapes
	
	def interpolate(self, frame, fraction):
		
		shapes = []
		
		for n, shape in enumerate(self.shapes):
		
			shapes.append(shape.interpolate(frame.shapes[n], fraction))
		
		return Frame(shapes)
	
	def draw(self, surf, pos):
		
		for shape in self.shapes:
			
			shape.draw(surf, pos)
	
class Frame_Shape():
	
	def __init__(self):
		pass
	
	def interpolatePoints(self, opoints, fraction):
		
		points = []
		
		for n in xrange(len(self.points)):
			
			p1, p2 = self.points[n], opoints[n]
			x = interpolate(p1.x, p2.x, fraction)
			y = interpolate(p1.y, p2.y, fraction)
			points.append(v2d(x, y))
		
		return points
	
	def interpolateColour(self, ocolour, fraction):
		
		r = interpolate(self.colour[0], ocolour[0], fraction)
		g = interpolate(self.colour[1], ocolour[1], fraction)
		b = interpolate(self.colour[2], ocolour[2], fraction)
		
		return (r, g, b)
	
	def interpolate(self, fshape, fraction):
		pass
	
	def draw(self, surf, pos):
		pass
	
class Frame_Line(Frame_Shape):
	
	def __init__(self, colour, p1, p2, thickness):
		
		self.colour = colour
		self.points = [p1, p2]
		self.thickness = thickness
	
	def interpolate(self, fline, fraction):
		
		if self.colour != fline.colour:
		
			colour = self.interpolateColour(fline.colour)
		
		else:
		
			colour = self.colour
		
		if self.points != fline.points:
			
			points = self.interpolatePoints(fline.points, fraction)
		
		else:
		
			points = [self.points[0],self.points[1]]
			
		if self.thickness != fline.thickness:
			
			thickness = int(interpolate(self.thickness, fline.thickness, fraction))
		
		else:
		
			thickness = self.thickness
		
		return Frame_Line(colour, points[0], points[1], thickness)
	
	def draw(self, surf, pos):
		
		pygame.draw.line(surf, self.colour, self.points[0]+pos, \
		                 self.points[1]+pos, self.thickness)
	
class Frame_Circle(Frame_Shape):
	
	def __init__(self, colour, position, radius, thickness):
		
		self.colour = colour
		self.position = position
		self.radius = radius
		self.thickness = thickness
	
	def interpolate(self, ocircle, fraction):
		
		colour = self.interpolateColour(ocircle.colour, fraction)
		x = interpolate(self.position.x, ocircle.position.x, fraction)
		y = interpolate(self.position.x, ocircle.position.y, fraction)
		position = v2d(x, y)
		radius = interpolate(self.radius, ocircle.radius)
		thickness = interpolate(self.thickness, ocircle.radius)
		
		return Frame_Circle(colour, position, radius, thickness)
	
	def draw(self, surf, pos):
		
		pygame.draw.circle(surf, self.colour, self.position+pos, self.radius, self.thickness)
	
def test():
	
	ANIM_Set_Interpolate_Mode(ANIM_MODE_LINEAR)
	
	points = []
	points.append((0,400))
	points.append((50,100))
	points.append((100,120))
	points.append((150,500))
	points.append((200,50))
	points.append((250,60))
	points.append((300,70))
	points.append((350,200))
	points.append((400,400))
	points.append((450,400))
	points.append((500,600))
	points.append((550,550))
	points.append((600,0))
	points.append((650,530))
	points.append((700,400))
	points.append((750,450))
	points.append((800,400))

	pygame.init()

	s = pygame.display.set_mode((800,600))
	
	detail = 50
	
	plotlist(s, points, detail)
	
	while 1:
		
		for e in pygame.event.get():
			
			if e.type == QUIT:
				
				pygame.quit()
				return
		
		pygame.display.update()

test()