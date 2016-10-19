#==============================================================================
# matrix.py
# Matrix stuff, yay
#
#==============================================================================

import operator, math

class Matrix(object):
	def __init__(self, rows):
		self.rows = rows
	
	def __len__(self):
		return len(self.rows[0])
	
	def __getitem__(self, index):
		return self.rows[index]
	
	def __getstate__(self):
		print "Getstate lol"
		return 0
	
	def __repr__(self):
		string = ""
		for row in self.rows:
			string += "[ "
			for item in row:
				string += str(item) + ", "
			string = string[:-2]
			string += " ]\n"
		return string
	
	def __neg__(self):
		new_rows = []
		for row in self.rows:
			new_row = []
			for item in row:
				new_row.append(-item)
			new_rows.append(new_row)
		return Matrix(new_rows)
	
	def __add__(self, b):
		try:
			x=b[0]
		except:
			return Matrix( map( lambda row: \
			map( lambda item: item + b, row), self.rows))
			
		if not (len(self.rows) == len(b.rows) and \
		len(self.rows[0]) == len(b.rows[0])):
			print "fail"; return
		
		row_counter = 0
		item_counter = 0
		new_rows = []
		
		while row_counter < len(self.rows):
			new_row = []
			
			while item_counter < len(self.rows[0]):
				new_row.append(self.rows[row_counter][item_counter] + \
				b.rows[row_counter][item_counter])
				
			new_rows.append(new_row)
			
		return Matrix(new_rows)
	
	def __sub__(self, b):
		return self + -b
	
	def __mul__(self, matrix):
		if len(self.rows) != len(matrix.rows[0]):
			print "fail"
			return
		
		row_counter = 0
		row_item_counter = 0
		column_item_counter = 0
		new_matrix = []
		
		while row_counter < len(self.rows):
			row_item_counter = 0
			new_row = []
			
			while row_item_counter < len(self.rows[0])-1:
				column_item_counter = 0
				new_row_item = 0
				
				while column_item_counter < len(matrix.rows):
					new_row_item += self.rows[row_counter][column_item_counter] * \
					matrix.rows[column_item_counter][row_item_counter]
					column_item_counter += 1
					
				new_row.append(new_row_item)
				row_item_counter += 1
				
			new_matrix.append(new_row)
			row_counter += 1
			
		return Matrix(new_matrix)
	
def TranslationMatrix3D(x,y,z):
	pass
def RotationMatrix3D(a,b,c):
	pass
def ScalingMatrix3D(x,y,z):
	pass
	
def main():
	A = Matrix([[1,0,2],[-1,3,1]])
	B = Matrix([[3,1],[2,1],[1,0]])
	print A
	print B
	
	print A*B
	
	print A + 2
	
	print A - 2

if __name__ == '__main__': main()