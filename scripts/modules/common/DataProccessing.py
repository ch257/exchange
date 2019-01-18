# -*- coding: utf-8 -*

# from modules.common.Tools import *

import time
import datetime
from datetime import datetime as dt, date, time as tm

class DataProccessing:
	
	def __init__(self, errors):
		self.errors = errors
	
	def generate_time_range(self, start, stop, step, exclude):
		time_range = []
		start_time = dt.strptime(start, '%H:%M:%S')
		stop_time = dt.strptime(stop, '%H:%M:%S')
		if stop_time == dt.strptime('00:00:00', '%H:%M:%S'): 
			stop_time = dt.strptime(stop, '%H:%M:%S') + datetime.timedelta(days=1)
		
		step_time = dt.strptime(step, '%H:%M:%S').time()
		step_time = datetime.timedelta(hours=step_time.hour, minutes=step_time.minute, seconds=step_time.second) #dt.strptime(step, '%H:%M:%S').time()
		
		curr_time = start_time
		while not self.errors.error_occured:
			if curr_time >= stop_time:
				break
			else:
				# print(curr_time.time())
				time_range.append(curr_time.time())
			curr_time += step_time
			
		print(time_range)
		return ''
		
	def join_time_range_with_data(self, time_range, data):
		pass