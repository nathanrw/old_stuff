import random

d6 = lambda : random.randrange(0,7)

class Gang(object):
	
	def __init__(self, name, house, stash):
		
		self.name = name
		self.house = house
		self.rating = 0
		self.stash = stash
		self.members = []
		self.territory = []
		self.items = []

class Unit(object):
	
	def __init__(self, name):
		
		self.name = name
		
		self.items = []
		self.skills = []
		self.injuries = []
		self.statmodifiers = []
	
	def addItem(self, item):
		
		pass
	
	def addSkill(self, skill):
		
		pass
	
	def addInjury(self, injury):
		
		pass

class Skill(object):
	
	def __init__(self, name, description):
		
		self.name = name
		self.description = description
		
class Injury(object):
	
	def __init__(self, name, description):
		
		self.name = name
		self.description = description
		
class Item(object):
	
	def __init__(self, name, profile, notes):
		
		self.name = name
		self.profile = profile
		self.notes = notesd

class StatModifier(object):
	
	def __init__(self, name, profile):
		
		self.name = name
		self.profile = profile