# -*- coding: utf-8 -*

from modules.common.Errors import *
from modules.common.FileSystem import *
from modules.common.SettingsReader import *
from modules.common.DataStream import *
from modules.common.DataProccessing import *


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
			settings_reader.read_ConcatinateData_settings(self.settings, ini_file_path, encoding)
	
	def main(self, args):
		self.read_settings(args)
		# print(self.settings)
		fs = FileSystem(self.errors)
		data_stream = DataStream(self.errors)
		dp = DataProccessing(self.errors)
		
		input_folder = self.settings['input']['folder']
		input_feed_format = self.settings[self.settings['input']['input_feed_format']]
		
		folder_list = fs.get_folder_list(input_folder)
		folder_list.sort()
		print(folder_list)
		
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')