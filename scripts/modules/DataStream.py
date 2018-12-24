# -*- coding: utf-8 -*

from modules.Files import *

class DataStream:
	
	def __init__(self, errors):
		self.errors = errors
		self.file_handler = None
	
	def open_stream(self, file_path, feed_format):
		if self.errors.error_occured:
			return None
		
		encoding = feed_format['encoding']
		self.file_handler = Files(self.errors)
		self.file_handler.open_file(file_path, 'r', encoding)
		
	def read_all(self, feed_format):
		if self.errors.error_occured:
			return {}
		
		data = {}
		
		return data
	
	def close_stream(self):
		if self.file_handler and not self.errors.error_occured:
			self.file_handler.close_file()