# -*- coding: utf-8 -*

from modules.common.Errors import *
# from modules.common.IniParser import *
from modules.common.SettingsReader import *
from modules.common.Tools import *
from modules.common.DataStream import *
from modules.common.Plotter import *

class Arbitrage:
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
			settings_reader.read_DataStraemSettings(self.settings, ini_file_path, encoding)
	
	def main(self, args):
		self.read_settings(args)
		
		print(self.settings)
		# data_stream = DataStream(self.errors)
		# input_file_path = self.settings['input']['file_path']
		# input_feed_format = self.settings[self.settings['input']['input_feed_format']]
		# data_stream.open_stream(input_file_path, input_feed_format)
		# data = data_stream.read_all(input_feed_format)
		# data_stream.close_stream()
		
		# print(data)
		
		# fig_name = '0000'
		# plotter = Plotter(self.errors)
		# plotter.plot_series(data, self.settings, fig_name)
		
		# print(data)
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')