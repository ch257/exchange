# -*- coding: utf-8 -*

class DataIterator:
	
	def __init__(self, errors, data, index_col, feed_format):
		self.errors = errors
		self.data = data
		self.index_col = index_col
		self.feed_format = feed_format
		self.rec_cnt = 0
		if self.errors.error_occured:
			self.EOD = True
		else:
			self.EOD = False
			
	def get_next_rec(self):
		rec = {}
		if self.rec_cnt < len(self.data[self.index_col]):
			for col in self.feed_format['columns']:
				rec[col] = self.data[col][self.rec_cnt]
			
			self.rec_cnt += 1
			if self.rec_cnt == len(self.data[self.index_col]):
				self.EOD = True
		else:
			self.EOD = True
		return rec
