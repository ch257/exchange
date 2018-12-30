# -*- coding: utf-8 -*


class Tools:
	def __init__(self, errors):
		self.errors = errors
	
	def explode(self, div, str):
		if div and str:
			return str.split(div)
		elif str:
			return [str]
		else:
			return []
	
	def implode(self, div, arr):
		str = div.join(arr)
		return str
	
	def line_to_record(self, div, line, keys):
		rec = {}
		arr = self.explode(div, line)
		if len(arr) < len(keys):
			for i in range(len(arr)):
				rec[keys[i]] = arr[i]
			self.errors.raise_error('not enough columns in line')
		else:
			for i in range(len(keys)):
				rec[keys[i]] = arr[i]
		return rec
	
	def record_to_line(self, div, rec, keys):
		line = None
		for key in keys:
			if rec[key]:
				item = rec[key]
			else:
				item = ''
			if line:
				line = line + div + item
			else:
				line = item
		return line

	def escape_sequence(self, str):
		if str:
			str = str.replace("'\\t'", '\t')
			str = str.replace("','", ',')
			str = str.replace("';'", ';')
			str = str.replace("''", '')
		return str
	
	def print_arr(self, arr):
		for arr_item in arr: 
			print(arr_item)
			
	def int_arr(self, arr):
		cnt = 0
		for item in arr:
			arr[cnt] = int(item)
			cnt = cnt + 1
		return arr
			
	def float_arr(self, arr):
		cnt = 0
		for item in arr:
			arr[cnt] = float(item)
			cnt = cnt + 1
		return arr
		
	def bool_arr(self, arr):
		cnt = 0
		for item in arr:
			if arr[cnt] == '1':
				arr[cnt] = True
			else:
				arr[cnt] = False
			cnt = cnt + 1
		return arr
		
	def format_number(self, zeros, number):
		len_zeros = len(zeros)
		str_number = str(number)
		len_number = len(str_number)
		return zeros[0:(len_zeros - len_number)] + str_number