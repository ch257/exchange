# -*- coding: utf-8 -*

class Buffer:
	
	def __init__(self, size):
		self.size = size
		self.buff = []
		self.is_ready = False
		
	def slide(self, new_item):
		if len(self.buff) < self.size:
			self.buff.append(new_item)
			if len(self.buff) == self.size:
				self.is_ready = True
		else:
			self.buff.append(new_item)
			self.buff.pop(0)
		
	def update(self, new_item):
		if len(self.buff) == self.size:
			self.buff.append(new_item)
	
