#==============================================================================
# avatar.py
# The player.
#
#==============================================================================

from planet import Planet
from thruster import Thruster
from maths import *

class Avatar(Planet):
	""" Used as a base for thiangs such as spaceships and missiles. """
	def __init__(self, pos):
		""" Them thar thrusters be lookin' dodgy. """
		
		self.state = "alive"
		
		self.pos = pos
		self.velocity = [0,0]
		self.omega = 0
		self.mass = 5.0
		self.reactionmass = 1.0
		self.density = 0
		self.rotation = 0
		#self.points = [[-10,-50],[5,-50],[5,-20],[10,-20],[10,30],[8,30],[12,50],[-12,50],[-8,30],[-12,30],[-12,-20],[-10,-20]]
		self.points = [[0,-50],[20,50],[-20,50]]
		self.radius = 30
		self.hull = 1.0
		
		self.target = 0
		
		s = 2.0
		
		self.thrusters = []
		
		self.thruster_fore_backward = Thruster(self,[0,-50],[0*s,1*s],1)
		self.thrusters.append(self.thruster_fore_backward)
		
		self.thruster_fore_right = Thruster(self,[0,-50],[-1*s,0*s],1)
		self.thrusters.append(self.thruster_fore_right)
		
		self.thruster_fore_left = Thruster(self,[0,-50],[1*s,0*s],1)
		self.thrusters.append(self.thruster_fore_left)
		
		self.thruster_rear_forward = Thruster(self,[0,50],[0*s,-1*s],1)
		self.thrusters.append(self.thruster_rear_forward)
		
		self.thruster_rear_right = Thruster(self,[0,50],[-1*s,0*s],1)
		self.thrusters.append(self.thruster_rear_right)
		
		self.thruster_rear_left = Thruster(self,[0,50],[1*s,0*s],1)
		self.thrusters.append(self.thruster_rear_left)
		
	def rotate(self,angle):
		""" One line function has one line. Oh, wait. """
		self.rotation += angle
	
	def get_moment(self):
		""" Hmm, dodginess. """
		CM = (self.thruster_fore_right.strength*self.thruster_fore_right.fraction/self.mass + \
			self.thruster_rear_left.strength*self.thruster_rear_left.fraction/self.mass)
		ACM  = (self.thruster_fore_left.strength*self.thruster_fore_left.fraction/self.mass + \
			self.thruster_rear_right.strength*self.thruster_rear_right.fraction/self.mass)
		return ACM - CM
	
	def aquire_target(self,obj):
		self.target = obj
	
	def angular_motion(self):
		self.omega += self.get_moment()
	
	def update(self):
		""" This comment is entirely useless. """
		if self.reactionmass > 0:
			for thruster in self.thrusters:
				if self.reactionmass > 0:
					thruster.thrust()
					self.reactionmass -= 0.001*thruster.strength*thruster.fraction
				else:
					thruster.fraction = 0
		self.angular_motion()
		self.rotate(self.omega*(pi/180)*2)
		self.move()