# -*- coding: utf-8 -*

from modules.common.Errors import *
from modules.common.FileSystem import *
from modules.common.SettingsReader import *
from modules.common.DataStream import *
from modules.common.DataProccessing import *
from modules.common.Tools import *


class JoinData:
	def __init__(self):
		self.errors = Errors()
		self.settings = {}
	
	def read_settings(self, args):
		if len(args) < 2:
			self.errors.raise_error('no ini file path')
		else:
			encoding = 'utf-8'
			if len(args) > 2:
				encoding = args[2]
				
			settings_reader = SettingsReader(self.errors)
			ini_file_path = args[1]
			settings_reader.read_JoinData_settings(self.settings, ini_file_path, encoding)
	
	def main(self, args):
		self.read_settings(args)
		# print(self.settings)
		fs = FileSystem(self.errors)
		data_stream = DataStream(self.errors)
		dp = DataProccessing(self.errors)
		
		tools = Tools(self.errors)
		
		input_folder = self.settings['input']['folder']
		input_feed_format = self.settings[self.settings['input']['input_feed_format']]
		input_columns = self.settings['input']['columns']
		
		output_folder = self.settings['output']['folder']
		output_file = self.settings['output']['file']
		output_feed_format = self.settings[self.settings['output']['output_feed_format']]
		
		# print(input_columns);
		
		folder_list = fs.get_folder_list(input_folder)
		folder_list.sort()
		cnt = 0
		files_number = len(folder_list)
		while not self.errors.error_occured and cnt < files_number:
			input_file_path = input_folder + folder_list[cnt]
			data_stream.open_stream(input_file_path, input_feed_format)
			data = data_stream.read_all(input_feed_format)
			data_stream.close_stream()
			if cnt == 0:
				start = '12:00:00'
				stop = '00:00:00'
				step = '00:05:00'
				exclude = [
					['18:50:00', '19:05:00']
				]
				time_range = dp.generate_time_range(start, stop, step, exclude)
				date_range = dp.select_date_range(data['<DATE>'])
				
			timed_data = dp.create_data_by_time_range(time_range, date_range, data, input_columns)
			print(timed_data);
			cnt += 1
		
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')