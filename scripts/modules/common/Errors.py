# -*- coding: utf-8 -*

class Errors:
	def __init__(self):
		self.errors = []
		self.error_occured = False
	
	def raise_error(self, description):
		self.error_occured = True
		self.errors.append(description)

	def print_errors(self):
		for error in self.errors:
			print('Error: ' + error)
		