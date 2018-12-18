# -*- coding: utf-8 -*

from modules.Errors import *

class Main:
	def __init__(self):
		self.errors = Errors()
	
	def main(self):
		print('Hello!')
		if self.errors.error_occured:
			self.errirs.print_errors()