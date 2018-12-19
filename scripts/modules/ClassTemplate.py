# -*- coding: utf-8 -*

from modules.Errors import *
from modules.IniParser import *

class ClassTemplate:
	def __init__(self):
		self.errors = Errors()
		self.ini_encoding = 'utf-8'
		self.settings = []
	
	def read_settings(self, args):
		if len(args) < 2:
			self.errors.raise_error('no ini file path')
		else:
			encoding = self.ini_encoding
			if len(args) > 2:
				encoding = args[2]
				
			ini_file_path = args[1]
			ini_parser = IniParser(self.errors)
			self.settings = ini_parser.read_ini(args[1], encoding)
	
	def main(self, args):
		self.read_settings(args)
			
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')