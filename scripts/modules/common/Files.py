# -*- coding: utf-8 -*


class Files:
	def __init__(self, errors):
		self.errors = errors
		self.handler = None
	
	def open_file(self, path, mode, encoding):
		if not self.errors.error_occured:
			try:
				self.handler = open(path, mode, encoding = encoding)
			except Exception as e:
				self.errors.raise_error('Can\'t open file ' + path)
	
	def close_file(self):
		if self.handler:
			self.handler.close()
			self.handler = None
	
	def read_line(self):
		return self.handler.readline()
	
	def write_line(self, line):
		self.handler.write(line + "\n")
		