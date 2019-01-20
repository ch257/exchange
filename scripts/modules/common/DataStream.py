# -*- coding: utf-8 -*

from modules.common.Files import *
from modules.common.Tools import *

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
		if value:
			if type == 'num':
				return float(value)
			elif type == 'int':
				return int(value)
			elif type == 'float':
				return float(value)
			elif type == 'yyyymmdd':
				return {
					'yyyymmdd':value,
					'yyyy': value[0:4],
					'yy': value[2:4],
					'mm': value[4:6],
					'dd': value[6:]
				}
			elif type == 'hhmmss':
				return {
					'hhmmss': value,
					'hh': value[0:2],
					'mm': value[2:4],
					'ss': value[4:]
				}
		else:
			value = None
		return value
	
	def type_record(self, rec, columns, types):
		for col_cnt in range(len(rec)):
			rec[columns[col_cnt]] = self.type_value(rec[columns[col_cnt]], types[col_cnt])
	
	def read_all(self, feed_format):
		if self.errors.error_occured:
			return {}
		
		skip_first_lines_number = feed_format['header_lines_number']
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
				if line:
					rec = self.tools.line_to_record(column_separator, line, columns)
					self.type_record(rec, columns, column_data_types)
					for col_cnt in range(len(rec)):
						data[columns[col_cnt]].append(rec[columns[col_cnt]])
			else:
				break
		return data
	
	def close_stream(self):
		if self.file_handler and not self.errors.error_occured:
			self.file_handler.close_file()