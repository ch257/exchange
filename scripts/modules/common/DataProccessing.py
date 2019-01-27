# -*- coding: utf-8 -*

# from modules.common.Tools import *

import time
import datetime
from datetime import datetime as dt, date, time as tm

class DataProccessing:
	
	def __init__(self, errors):
		self.errors = errors
	
	def time_range(self, start, stop, step):
		rng = []
		start_time = dt.strptime(start, '%H:%M:%S')
		stop_time = dt.strptime(stop, '%H:%M:%S')
		if stop_time == dt.strptime('00:00:00', '%H:%M:%S'): 
			stop_time = dt.strptime(stop, '%H:%M:%S') + datetime.timedelta(days=1)
		step_time = dt.strptime(step, '%H:%M:%S').time()
		step_time = datetime.timedelta(hours=step_time.hour, minutes=step_time.minute, seconds=step_time.second)
		
		curr_time = start_time
		while not self.errors.error_occured:
			if curr_time >= stop_time:
				break
			else:
				rng.append(curr_time.time())
			curr_time += step_time
		
		return rng
	
	def generate_time_range(self, start, stop, step, exclude=[]):
		rng = []
		start_time = dt.strptime(start, '%H:%M:%S')
		stop_time = dt.strptime(stop, '%H:%M:%S')
		if stop_time == dt.strptime('00:00:00', '%H:%M:%S'): 
			stop_time += datetime.timedelta(days=1)
		step_time = dt.strptime(step, '%H:%M:%S').time()
		step_time = datetime.timedelta(hours=step_time.hour, minutes=step_time.minute, seconds=step_time.second)
		
		for excl_cnt in range(len(exclude)):
			excl = exclude[excl_cnt].split('-')
			excl[0] = dt.strptime(excl[0], '%H:%M:%S')
			excl[1] = dt.strptime(excl[1], '%H:%M:%S')
			if excl[1] == dt.strptime('00:00:00', '%H:%M:%S'):
				excl[1] += datetime.timedelta(days=1)
			
			exclude[excl_cnt] = [excl[0], excl[1]]

		curr_time = start_time
		while not self.errors.error_occured:
			if curr_time >= stop_time:
				break
			else:
				in_exclude = False
				for excl in exclude: 
					if excl[0] <= curr_time and excl[1] > curr_time:
						in_exclude = True
						break
				if not in_exclude:
					rng.append(tm.strftime(curr_time.time(), '%H%M%S'))
			curr_time += step_time
		
		return rng
		
	def select_date_range(self, dates):
		date_rng = []
		curr_date = ''
		for cd in dates:
			if curr_date != cd['yyyymmdd']:
				date_rng.append(cd['yyyymmdd'])
				curr_date = cd['yyyymmdd']
		
		return date_rng
		
	def create_data_by_time_range(self, time_range, date_range, data, columns):
		timed_data = {}
		timed_data['<DATE>'] = [] 
		timed_data['<TIME>'] = []
		for col in columns:
			timed_data[col] = []
		
		cnt = 0
		data_length = len(data['<DATE>'])
		for c_date in date_range:
			for c_time in time_range:
				timed_data['<DATE>'].append(c_date)
				timed_data['<TIME>'].append(c_time)
				found = False
				while cnt < data_length:
					if data['<DATE>'][cnt]['yyyymmdd'] == c_date:
						if data['<TIME>'][cnt]['hhmmss'] == c_time:
							# print(data['<DATE>'][cnt]['yyyymmdd'], c_date, data['<TIME>'][cnt]['hhmmss'], c_time)
							found = True
							break
						elif data['<TIME>'][cnt]['hhmmss'] > c_time:
							cnt -= 1
							break
					elif data['<DATE>'][cnt]['yyyymmdd'] > c_date:
						cnt -= 1
						break
					cnt += 1
					
				if found:
					for col in columns:
						timed_data[col].append(data[col][cnt])
				else:
					for col in columns:
						timed_data[col].append(None)
					
				# print(c_date, c_time)
				
		
		return timed_data
		# print(time_range)
		# print(date_range)
		
	def append_data(self, data, app_data):
		for key in data:
			data[key].extend(app_data[key])
