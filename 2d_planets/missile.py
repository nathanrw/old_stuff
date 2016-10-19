#==============================================================================
# missile.py
# SHHHHWEEEBOOOOM!
#
#==============================================================================

from avatar import Avatar
from math import atan
from maths import *

class Missile(Avatar):
	""" SHHHWEEEEEWBOOOOOM! """
	def __init__(self,pos,velocity,angle, target):
		""" Target is a reference to the target - so it is tracked. """
		Avatar.__init__(self, pos)
		self.velocity = Add2DVector([0,0],velocity)
		self.rotation = angle
		self.target = target
		self.mass = 0.1
		for thruster in self.thrusters:
			thruster.strength = 0.25
			thruster.fraction = 0.0
		self.thruster_rear_forward.fraction = 0.2
		self.points = [[0,-25],[10,25],[-10,25]]
		self.radius = 3
		self.counter = 0
	
	def turnleft(self, degree=1):
		self.thruster_rear_left.fraction = 0.1*degree
		self.thruster_fore_right.fraction = 0.1*degree
		self.thruster_fore_left.fraction = 0
		self.thruster_rear_right.fraction = 0
		
	def turnright(self, degree=1):
		self.thruster_rear_left.fraction = 0
		self.thruster_fore_right.fraction = 0
		self.thruster_fore_left.fraction = 0.1*degree
		self.thruster_rear_right.fraction = 0.1*degree
		
	def ai(self):
		direction = Rotate2DVector([1,0],self.rotation)
		required_direction = Unit2DVector(Sub2DVector(self.target.pos,self.pos))
		cos_angle = DotProduct2DVector(direction,required_direction)
		
		if cos_angle > 0:
			self.turnright()
		elif cos_angle < 0:
			self.turnleft()
	
	def fuel(self):
		if self.counter > 100:
			self.state = "dead"
			for thruster in self.thrusters:
				thruster.state = "dead"
		self.counter+=1
	
	def update(self):
		Avatar.update(self)
		self.ai()
		self.fuel()
	
	def update2(self):
		if self.rotation > twopi:
			self.rotation = 0
		elif self.rotation < 0:
			self.rotation = twopi
		self.move()
	
	def collide(self, obj, combine=1):
		if Avatar.collide(self, obj, combine):
			self.update = self.update2
			return 1
		return 0