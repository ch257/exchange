# -*- coding: utf-8 -*

from modules.indicators.Buffer import *

class SMA:
	
	def __init__(self, avg_per):
		self.avg_per = avg_per if avg_per > 0 else 1
		self.rolling_sum = 0
		self.buffer = Buffer(avg_per)
		self.last_mode = None

	
	def calc(self, new_item):
		sma_val = None
		if self.last_mode == 'u':
			self.rolling_sum = self.rolling_sum + new_item - self.buffer.buff[0] + self.buffer.buff[self.buffer.size]
		else: 
			self.rolling_sum = self.rolling_sum + new_item
		
		self.buffer.slide(new_item)
		self.last_mode = 'c'
		if self.buffer.is_ready:
			sma_val = self.rolling_sum / self.avg_per
			self.rolling_sum = self.rolling_sum - self.buffer.buff[0]
		
		return sma_val

