import pygame
from pygame.locals import *
import math
import random
from vec2d import vec2d as v2d

def draw_arrow(surf, colour, a, b, thickness=1):
	pygame.draw.aaline(surf, colour, a, b, thickness)
	l = (b-a).length
	s = l*0.25
	if s > 10: s = 10
	dir = (b-a).unit()
	pygame.draw.aaline(surf, colour, b, b-dir.rotated( 30)*s, thickness)
	pygame.draw.aaline(surf, colour, b, b-dir.rotated(-30)*s, thickness)

class Bullet():
	
	traillength = 0.003
	
	def __init__(self, pos, vel, *groups):
		
		self.pos = pos
		self.vel = vel
		self.prevpos = v2d(pos)
		
		self.groups = []
		
		for group in groups:
			group.append(self)
			self.groups.append(group)
		
		self.k = self.traillength
		self.t = self.k
	
	def draw(self, surf):
		
		a = self.pos -self.vel.unit().rotated(30)*4
		b = self.pos -self.vel.unit().rotated(-30)*4
		pygame.draw.polygon(surf, (255,255,255), (self.pos,a,self.prevpos,b))

class Particle():
	
	lifetime = 0.3
	
	def __init__(self, pos, vel, *groups):
		
		self.pos = pos
		self.vel = vel
		
		self.groups = []
		for group in groups:
			group.append(self)
			self.groups.append(group)
		
		self.t = 0
	
	def update(self, dt):
		
		self.t += dt
		if self.t >= self.lifetime:
			self.kill()
		
		self.pos += self.vel * dt
	
	def kill(self):
		for group in self.groups:
			group.remove(self)
			self.groups.remove(group)
	
	def draw(self, surf):
		
		surf.set_at(self.pos, (255,255,255))

class Main():
	
	screenrect = Rect(0,0,1680,1050)
	
	def __init__(self):
		
		pygame.init()
		
		self.display = pygame.display.set_mode(self.screenrect.size)
		
		self.bullets = []
		self.particles = []
		
		self.dt = 0
		
		self.angle = 0
		
		self.shooting = 0
		
		self.goingRight = 0
		self.goingLeft = 0
		
		self.clock = pygame.time.Clock()
		
		self.rof = 7.0
		self.firecounter = 0
		
		self.wall = pygame.Surface(self.screenrect.size, SRCALPHA)
		
		self.brush = pygame.Surface((10,10), SRCALPHA)
		pygame.draw.circle(self.brush, (255,255,255), (5,5), 5)
		
		self.wallMask = pygame.mask.Mask(self.screenrect.size)
		self.brushMask = pygame.mask.from_surface(self.brush)
		
		self.painting = 0
		
		self.hitMask = pygame.mask.Mask((3,3))
		self.hitMask.fill()
		
		self.playerimg = pygame.image.load("lolplayer.PNG")
		self.playerimg.set_colorkey((0,0,0))
		
		self.spinners = []
		
	def draw_player(self):
		
		rotated = pygame.transform.rotate(self.playerimg, -self.angle)
		rect = rotated.get_rect()
		rect.center = pygame.mouse.get_pos()
		self.display.blit(rotated, rect)
	
	def handleEvents(self):
		
		for e in pygame.event.get():
			
			if e.type == QUIT:
				pygame.quit()
				return 0
			
			elif e.type == KEYDOWN:
				
				if e.key == K_a:
					
					self.goingLeft = 1
				
				elif e.key == K_d:
					
					self.goingRight = 1
			
			elif e.type == KEYUP:
				
				if e.key == K_a:
					
					self.goingLeft = 0
					
				elif e.key == K_d:
					
					self.goingRight = 0
			
			elif e.type == MOUSEBUTTONDOWN:
				
				if e.button == 3:
					self.painting = 1
					self.paintpos = v2d(pygame.mouse.get_pos())
				elif e.button == 1:
					self.shooting = 1
					self.firecounter = 1.0/self.rof
				
			elif e.type == MOUSEBUTTONUP:
				
				if e.button == 3:
					self.painting = 0
				elif e.button == 1:
					self.shooting = 0
		
		return 1
	
	def paint(self):
		#p = v2d(pygame.mouse.get_pos()) - v2d(self.brush.get_rect().size)*0.5
		#self.wallMask.draw(self.brushMask, p)
		#self.wall.blit(self.brush, p)
		
		self.oldpaintpos = self.paintpos
		self.paintpos = v2d(pygame.mouse.get_pos())
		
		pygame.draw.line(self.wall, (255,255,255), self.paintpos, self.oldpaintpos, 10)
		pygame.draw.circle(self.wall, (255,255,255), self.paintpos, 5)
		pygame.draw.circle(self.wall, (255,255,255), self.oldpaintpos, 5)
		
		self.wallMask = pygame.mask.from_surface(self.wall)
		
		self.bounding_rects = self.wallMask.get_bounding_rects()
	
	def shoot(self):
		
		while self.firecounter >= 1.0/self.rof:
			k = 3
			s = 3000
			
			p = v2d(pygame.mouse.get_pos()) + (v2d(61,45) - v2d(self.playerimg.get_rect().size)/2).rotated(self.angle)
			v = v2d(s, 0).rotated(self.angle).rotated(random.choice((1,-1))*random.random()*k)
			Bullet(p,v,self.bullets)
			self.firecounter -= 1.0/self.rof
	
	def findNearestHit(self, bullet):
		
		step = bullet.vel.unit()
		pos = v2d(bullet.pos)
		
		for n in xrange(bullet.vel.length*self.dt):
			
			hit = self.wallMask.get_at(pos.int())
			
			if hit: return pos
			
			pos += step
			if not self.screenrect.collidepoint(pos):
				return 0
		
		return 0
	
	def findNearestSpinnerHit(self, bullet):
		
		step = bullet.vel.unit()
		pos = v2d(bullet.pos)
		
		spinner = None
		sphit = None
		for spinner in self.spinners:
			for n in xrange(bullet.vel.length*self.dt):
				
				hit = spinner.ishit(pos)
				
				if hit: sphit = pos
				
				pos += step
				if not self.screenrect.collidepoint(pos):
					return 0, 0
		return sphit, spinner
	
	def update(self):
		
		a = 400
		
		if self.goingLeft and self.goingRight:
			pass
		elif self.goingLeft:
			self.angle -= a*self.dt
		elif self.goingRight:
			self.angle += a*self.dt
		
		if self.painting:
			self.paint()
		
		if self.shooting:
			self.firecounter += self.dt
			self.shoot()
		else:
			self.firecounter = 0
		
		for particle in self.particles:
			
			particle.update(self.dt)
		
		for bullet in self.bullets:
			
			if not self.screenrect.collidepoint(bullet.pos):
				self.bullets.remove(bullet)
				continue
			
			impactPoint = self.findNearestHit(bullet)
			impact2, impactSpinner = self.findNearestSpinnerHit(bullet)
			if impactPoint or ((impactPoint and impact2) and (impactPoint-bullet.pos).length < (impact2-bullet.pos).length()):
				
				p = impactPoint - v2d(1,1)
				
				a = self.wallMask.overlap_area(self.hitMask, p)
				
				nX = a - self.wallMask.overlap_area(self.hitMask, p+v2d(0,1))
				nY = a - self.wallMask.overlap_area(self.hitMask, p+v2d(1,0))
				
				normal = v2d(nY, nX).unit()
				
				bullet.prevpos = bullet.pos
				bullet.pos = impactPoint - bullet.vel.unit()
				bullet.vel = normal.reflect(bullet.vel) * 0.6
				bullet.pos += bullet.vel.unit()*5
				if bullet.vel.length < 500:
					self.bullets.remove(bullet)
				
				for x in xrange(5):
					Particle(v2d(impactPoint), normal.rotated(random.choice((45,-45))*random.random())*100, self.particles)
			
			elif impact2:
				
				pass
			
			else:
				bullet.t += self.dt
				
				if bullet.t >= bullet.k:
					bullet.t -= bullet.k
					bullet.prevpos = v2d(bullet.pos)
				bullet.pos += bullet.vel * self.dt
				bullet.vel += v2d(0,10)
				bullet.vel.x*=0.99
	
	def draw(self):
		
		self.display.fill((0,0,0))
		
		self.display.blit(self.wall, (0,0))
		
		for bullet in self.bullets:
			
			bullet.draw(self.display)
			
		for particle in self.particles:
			
			particle.draw(self.display)
			
		p = v2d(pygame.mouse.get_pos())
		p2 = p + v2d(50,0).rotated(self.angle)
		#draw_arrow(self.display, (255,255,255), p, p2)
		self.draw_player()
		
		pygame.display.update()
	
	def mainLoop(self):
		
		t1 = 0
		t2 = 0
		
		while self.handleEvents():
			
			t1 = pygame.time.get_ticks()
			
			self.dt = (t1 - t2)/1000.0
			
			self.update()
			self.draw()
			
			t2 = t1
			
			self.clock.tick(60)

Main().mainLoop()