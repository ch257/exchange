# -*- coding: utf-8 -*

from modules.common.Errors import *
from modules.common.IniParser import *
from modules.common.Tools import *
from modules.common.DataStream import *
from modules.common.Plotter import *

class Plot:
	def __init__(self):
		self.errors = Errors()
		self.ini_encoding = 'utf-8'
		self.ini_parser = IniParser(self.errors)
		self.settings = {}
	
	def read_settings(self, args):
		if len(args) < 2:
			self.errors.raise_error('no ini file path')
		else:
			encoding = self.ini_encoding
			if len(args) > 2:
				encoding = args[2]
				
			ini_file_path = args[1]
			self.ini_parser.read_ini(args[1], encoding)
	
	def set_params(self, args):
		tools = Tools(self.errors)
		self.read_settings(args)
		self.settings['input'] = {}
		self.settings['input']['file_path'] = self.ini_parser.get_param('input', 'file_path')
		self.settings['input']['input_feed_format'] = self.ini_parser.get_param('input', 'input_feed_format')
		
		self.settings['output'] = {}
		self.settings['output']['folder'] = self.ini_parser.get_param('output', 'folder')
		
		input_feed_format = self.settings['input']['input_feed_format']
		self.settings[input_feed_format] = {}
		self.settings[input_feed_format]['encoding'] = self.ini_parser.get_param(input_feed_format, 'encoding')
		self.settings[input_feed_format]['header_lines_number'] = self.ini_parser.get_param(input_feed_format, 'header_lines_number', 'int')
		self.settings[input_feed_format]['columns'] = tools.explode(',', self.ini_parser.get_param(input_feed_format, 'columns'))
		self.settings[input_feed_format]['column_separator'] = tools.escape_sequence(self.ini_parser.get_param(input_feed_format, 'column_separator'))
		self.settings[input_feed_format]['column_data_types'] = tools.explode(',', self.ini_parser.get_param(input_feed_format, 'column_data_types'))
		
		self.settings['plotter'] = {}
		self.settings['plotter']['fig_folder'] = self.settings['output']['folder'] + self.ini_parser.get_param('plotter', 'fig_folder')
		self.settings['plotter']['series'] = tools.explode(',', self.ini_parser.get_param('plotter', 'series'))
		self.settings['plotter']['subplot_height_share'] = tools.int_arr(tools.explode(',', self.ini_parser.get_param('plotter', 'subplot_height_share')))
		self.settings['plotter']['subplots_number'] = self.ini_parser.get_param('plotter', 'subplots_number', 'int') 
		
		#check some params
		columns_number = str(len(self.settings[input_feed_format]['columns']))
		column_data_types_number = str(len(self.settings[input_feed_format]['column_data_types']))
		if columns_number != column_data_types_number:
			self.errors.raise_error('columns number(' + columns_number + ') is not equal column_data_types number(' +  column_data_types_number+ ')')
			
	
	def main(self, args):
		self.set_params(args)
		data_stream = DataStream(self.errors)
		input_file_path = self.settings['input']['file_path']
		input_feed_format = self.settings[self.settings['input']['input_feed_format']]
		data_stream.open_stream(input_file_path, input_feed_format)
		data = data_stream.read_all(input_feed_format)
		data_stream.close_stream()
		
		fig_name = '0000'
		plotter = Plotter(self.errors)
		plotter.plot_series(data, self.settings, fig_name)
		
		# print(data)
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')