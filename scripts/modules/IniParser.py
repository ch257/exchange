# -*- coding: utf-8 -*

from modules.Files import *

class IniParser:
	def __init__(self, errors):
		self.errors = errors
		self.settiings = {}
	
	def exlude_non_data(self, line):
		line = line.rstrip('\n')
		line = line.rstrip('\r')
		start_comment_pos = line.find(';')
		if start_comment_pos > -1:
			line = line[0:start_comment_pos]
		line = line.replace('\t', '')
		line = line.replace(' ', '')
		return line
		
	def read_ini(self, ini_file_path, encoding):
		if self.errors.error_occured:
			return self.settiings
		
		ini_file = Files(self.errors)
		ini_file.open_file(ini_file_path, 'r', encoding)
		while not self.errors.error_occured:
			line = ini_file.read_line()
			if line:
				line = self.exlude_non_data(line)
				
				print(line)
			else:
				break
		ini_file.close_file()
		return self.settiings