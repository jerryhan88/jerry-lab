class Node:
	def __init__(self):
		self.nid = 'n12'
		self.x, self.y = 100, 200
		self.other_attr = 1000
	def duplicate(self):
		n1 = Node(self.nid, self.x, self.y)
		attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
		for attr_name, value in [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]:
			if attr_name in ['nid', 'x', 'y']:
				continue
			setattr(n1, attr_name, value)			
		return n1
		
class Network():
	def duplicate():
		N1 = Network()
		N1.nodes = [n.duplicate() for n in self.nodes]