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
		input_column_data_types  = self.settings['input']['column_data_types']
		
		output_folder = self.settings['output']['folder']
		output_file = self.settings['output']['file']
		output_file_path = output_folder + output_file
		output_feed_format = self.settings[self.settings['output']['output_feed_format']]
		
		# print(input_columns);
		
		folder_list = fs.get_folder_list(input_folder)
		folder_list.sort()
		file_cnt = 0
		files_number = len(folder_list)
		joined_data = {}
		timed_data = {}
		
		joined_data['<DATE>'] = []
		joined_data['<TIME>'] = []
		for file_cnt in range(files_number):
			for col_cnt in range(len(input_columns)):
				joined_data[input_columns[col_cnt] + '_' + str(file_cnt + 1)] = []
				output_feed_format['columns'].append(input_columns[col_cnt] + '_' + str(file_cnt + 1))
				output_feed_format['column_data_types'].append(input_column_data_types[col_cnt])
				
		start = '12:00:00'
		stop = '00:00:00'
		step = '00:05:00'
		exclude = [
			['18:50:00', '19:05:00']
		]
		
		file_cnt = 0
		while not self.errors.error_occured and file_cnt < files_number:
			input_file_path = input_folder + folder_list[file_cnt]
			data_stream.open_stream(input_file_path, input_feed_format)
			data = data_stream.read_all(input_feed_format)
			data_stream.close_stream()
			if file_cnt == 0:
				time_range = dp.generate_time_range(start, stop, step, exclude)
				date_range = dp.select_date_range(data['<DATE>'])

			timed_data[file_cnt] = dp.create_data_by_time_range(time_range, date_range, data, input_columns)
			file_cnt += 1
		
		# print(len(timed_data[0]['<DATE>']))
		# print(len(timed_data[1]['<DATE>']))
		# print(len(timed_data[2]['<DATE>']))
		
		rec_cnt = 0
		for c_date in date_range:
			for c_time in time_range:
				rec = {}
				for file_cnt in range(files_number):
					for col in input_columns:
						if timed_data[file_cnt][col][rec_cnt] != None:
							rec[col + '_' + str(file_cnt + 1)] = timed_data[file_cnt][col][rec_cnt]
						else:
							rec = {}
							break
					if len(rec) == 0:
						break
						
				if len(rec) > 0:
					joined_data['<DATE>'].append(c_date)
					joined_data['<TIME>'].append(c_time)
					for k in rec:
						joined_data[k].append(rec[k])
					
				rec_cnt += 1
		
		data_stream.open_stream(output_file_path, output_feed_format, mode='w')
		data_stream.write_all(joined_data, output_feed_format)
		data_stream.close_stream()
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')