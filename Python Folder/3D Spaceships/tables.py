#Lookup Tables
import math

class Table():
	def __init__(self,data):
		self.data = data
		
def CosTable(accuracy):
	table = []
	for x in range(0,accuracy+1):
		table.append(math.cos(x*math.pi/accuracy))
	return table
def SineTable(accuracy):
	table = []
	for x in range(0,accuracy+1):
		table.append(math.sin(x*math.pi/accuracy))
	return table

costable = CosTable(1000)
sinetable = SineTable(1000)

def get_sine(x):
	pass
def get_cos(x):
	pass