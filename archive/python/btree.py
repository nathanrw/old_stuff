# A binary ordered tree example

class Node:
	left , right, data = None, None, 0
	
	def __init__(self, data):
		# initializes the data members
		self.left = None
		self.right = None
		self.data = data

class OrderedBinaryTree:
	def __init__(self, compare_less_than=lambda x, y: x <= y):
		# initializes the root member
		self.root = None
		self.compare_less_than = compare_less_than
	
	def addNode(self, data):
		# creates a new node and returns it
		return Node(data)
	
	def treeInsert(self, data):
		self.subtreeInsert(self.root, data)
	
	def subtreeInsert(self, root, data):
		# inserts a new data
		if root == None:
			# it there isn't any data
			# adds it and returns
			return self.addNode(data)
		else:
			# enters into the tree
			if self.compare_less_than(data,root.data):
				# if the data is less than the stored one
				# goes into the left-sub-tree
				root.left = self.subtreeInsert(root.left, data)
			else:
				# processes the right-sub-tree
				root.right = self.subtreeInsert(root.right, data)
			return root
	
	def treeLookup(self, target):
		return self.subtreeLookup(self.root, target)
	
	def subtreeLookup(self, root, target):
		# looks for a value into the tree
		if root == None:
			return 0
		else:
			# if it has found it...
			if target == root.data:
				return 1
			else:
				if target < root.data:
					# left side
					return self.subtreeLookup(root.left, target)
				else:
					# right side
					return self.subtreeLookup(root.right, target)
	
	def treeMinValue(self):
		return self.subtreeMinValue(self.root)
	
	def subtreeMinValue(self, root):
		# goes down into the left
		# arm and returns the last value
		while(root.left != None):
			root = root.left
		return root.data
	
	def treeMaxDepth(self):
		return self.subtreeMaxDepth(self.root)
	
	def subtreeMaxDepth(self, root):
		if root == None:
			return 0
		else:
			# computes the two depths
			ldepth = self.subtreeMaxDepth(root.left)
			rdepth = self.subtreeMaxDepth(root.right)
			# returns the appropriate depth
			return max(ldepth, rdepth) + 1
	
	def treeSize(self):
		return self.subtreeSize(self.root)
	
	def subtreeSize(self, root):
		if root == None:
			return 0
		else:
			return self.subtreeSize(root.left) + 1 + self.subtreeSize(root.right)
	
	def treeToList(self):
		return self.subtreeToList(self.root)
	
	def subtreeToList(self, root):
		if root == None:
			return []
		else:
			list = []
			list += self.subtreeToList(root.left)
			list.append(root.data)
			list += self.subtreeToList(root.right)
			return list
	
	def printTree(self):
		self.printSubtree(self.root)
	
	def printSubtree(self, root):
		# prints the tree path
		if root == None:
			pass
		else:
			self.printSubtree(root.left)
			print root.data,
			self.printSubtree(root.right)

	def printRevTree(self):
		self.printRevSubtree(self.root)

	def printRevSubtree(self, root):
		# prints the tree path in reverse
		# order
		if root == None:
			pass
		else:
			self.printRevSubtree(root.right)
			print root.data,
			self.printRevSubtree(root.left)
