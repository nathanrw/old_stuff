#==============================================================================
# The amazing bnp searcher thing.
#
#==============================================================================

from __future__ import with_statement

class BNPMember():
	def __init__(self, fields):
		self.fields = fields
	def __repr__(self):
		string = ""
		for field in self.fields:
			string += field + "\n"
		return string
	def check(self, match=["","","","","",""]):
		try:
			i = 0
			while i < len(match):
				if not (match[i] == self.fields[i] or match[i] == ""):
					return 0
				i += 1
			return 1
		except:
			return 0

class BNPList():
	def __init__(self, loc, other=0):
		if other is not 0:
			self.records = other
			return
		self.records = []
		with open(loc, "r") as f:
			lines = f.readlines()
			line_counter = 0
			eof = len(lines)
			record = []
			while line_counter < eof:
				if lines[line_counter] != "\n":
					record.append(lines[line_counter][:-1])
				else:
					self.records.append(BNPMember(record))
					record = []
				line_counter += 1
				
	def get_records(self):
		return self.records
	
	def search(self, match):
		matches = []
		for record in self.records:
			if record.check(match):
				matches.append(record)
		return BNPList(0,matches)
	
	def __repr__(self):
		string = ""
		for record in self.records:
			string += record.__repr__() + "\n"
		return string
	
def main():
	print BNPList("bnp.txt").search(["","","","","Dudley",""])

if __name__ == '__main__': main()
