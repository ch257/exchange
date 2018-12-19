# -*- coding: utf-8 -*

from modules.Files import *

class IniParser:
	def __init__(self, errors):
		self.errors = errors
	
	def read_ini(self, ini_file_path, encoding):
		ini_file = Files(self.errors)
		ini_file.open_file(ini_file_path, 'r', encoding)
		ini_file.close_file()