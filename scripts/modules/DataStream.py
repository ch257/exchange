# -*- coding: utf-8 -*

from modules.Files import *
from modules.Tools import *

class DataStream:
	
	def __init__(self, errors):
		self.errors = errors
		self.file_handler = None
		self.tools = Tools(self.errors)
	
	def open_stream(self, file_path, feed_format):
		if self.errors.error_occured:
			return None
		
		encoding = feed_format['encoding']
		self.file_handler = Files(self.errors)
		self.file_handler.open_file(file_path, 'r', encoding)
		
	def type_value(self, value, type):
		if type == 'num':
			return float(value)
		elif type == 'int':
			return int(value)
		elif type == 'float':
			return float(value)
		elif type == 'yyyymmdd':
			return value
		elif type == 'hhmmss':
			return value
		return value
	
	def type_record(self, rec, columns, types):
		col_cnt = 0
		for col in columns:
			rec[col] = self.type_value(rec[col], types[col_cnt])
			col_cnt += 1
	
	def read_all(self, feed_format):
		if self.errors.error_occured:
			return {}
		
		skip_first_lines_number = feed_format['skip_first_lines_number']
		columns = feed_format['columns']
		column_separator = feed_format['column_separator']
		column_data_types = feed_format['column_data_types']
		
		while skip_first_lines_number > 0 and not self.errors.error_occured:
			line = self.file_handler.read_line()
			skip_first_lines_number -= 1
		
		data = {}
		for col in columns:
			data[col] = []
		
		while not self.errors.error_occured:
			line = self.file_handler.read_line()
			if line:
				line = line.rstrip('\n')
				rec = self.tools.line_to_record(column_separator, line, columns)
				self.type_record(rec, columns, column_data_types)
				for col in columns:
					data[col].append(rec[col])
			else:
				break
		return data
	
	def close_stream(self):
		if self.file_handler and not self.errors.error_occured:
			self.file_handler.close_file()