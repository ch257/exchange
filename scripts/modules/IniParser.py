# -*- coding: utf-8 -*

from modules.Files import *

class IniParser:
	def __init__(self, errors):
		self.errors = errors
		self.settiings = {}
	
	def read_ini(self, ini_file_path, encoding):
		if self.errors.error_occured:
			return self.settiings
		
		ini_file = Files(self.errors)
		ini_file.open_file(ini_file_path, 'r', encoding)
		while not self.errors.error_occured:
			line = ini_file.read_line()
			if line:
				print(line)
			else:
				break
		ini_file.close_file()
		return self.settiings