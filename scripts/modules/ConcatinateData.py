# -*- coding: utf-8 -*

from modules.common.Errors import *
from modules.common.FileSystem import *
from modules.common.SettingsReader import *
from modules.common.DataStream import *
from modules.common.DataProccessing import *


class ConcatinateData:
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
			settings_reader.read_ConcatinateData_settings(self.settings, ini_file_path, encoding)
	
	def main(self, args):
		self.read_settings(args)
		# print(self.settings)
		fs = FileSystem(self.errors)
		input_folder = self.settings['input']['folder']
		input_feed_format = self.settings[self.settings['input']['input_feed_format']]
		columns = input_feed_format['columns']
		folder_list = fs.get_folder_list(input_folder)
		folder_list.sort()
		data_stream = DataStream(self.errors)
		dp = DataProccessing(self.errors)
		concatinated_data = {}
		for col in columns:
			concatinated_data[col] = []
		for file in folder_list:
			input_file_path = input_folder + file
			data_stream.open_stream(input_file_path, input_feed_format)
			data = data_stream.read_all(input_feed_format)
			data_stream.close_stream()
			dp.append_data(concatinated_data, data)
		
		output_folder = self.settings['output']['folder']
		output_file = self.settings['output']['file']
		output_file_path = output_folder + output_file
		output_feed_format = self.settings[self.settings['output']['output_feed_format']]
		fs.create_folder_branch(output_folder)
		data_stream.open_stream(output_file_path, output_feed_format, mode='w')
		data_stream.write_all(concatinated_data, output_feed_format)
		data_stream.close_stream()
		# print(concatinated_data)
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')