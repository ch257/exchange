# -*- coding: utf-8 -*

from modules.Errors import *
from modules.Files import *

class Main:
	def __init__(self):
		self.errors = Errors()
	
	def main(self, args):
		if len(args) < 2:
			self.errors.raise_error('no ini file path')
		
		file = Files(self.errors)
		file.open_file('settings/test.ini', 'r', 'utf-8')
		file.close_file()
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')