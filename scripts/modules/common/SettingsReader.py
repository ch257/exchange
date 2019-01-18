# -*- coding: utf-8 -*

from modules.common.IniParser import *
from modules.common.Tools import *

class SettingsReader:
	def __init__(self, errors):
		self.errors = errors
		self.settings = {}
		self.ini_encoding = 'utf-8'
		self.ini_parser = IniParser(self.errors)
		self.tools = Tools(self.errors)
		
	def compare_elements_number(self, settings, section1, param1, section2, param2):
		if self.errors.error_occured:
			return None
		elements_number1 = len(settings[section1][param1])
		elements_number2 = len(settings[section2][param2])
		if elements_number1 != elements_number2:
			self.errors.raise_error('[' + section1 + '][' + param1 + '] elements number(' + str(elements_number1) + ') is not equal [' + section2 + '][' + param2 + '] elements number(' +  str(elements_number2) + ')')
		
	def read_DataStraemSettings(self, settings, ini_file_path, encoding):
		self.ini_parser.read_ini(ini_file_path, encoding)
		settings['input'] = {}
		settings['input']['file_path'] = self.ini_parser.get_param('input', 'file_path')
		settings['input']['input_feed_format'] = self.ini_parser.get_param('input', 'input_feed_format')
		
		input_feed_format = settings['input']['input_feed_format']
		settings[input_feed_format] = {}
		settings[input_feed_format]['encoding'] = self.ini_parser.get_param(input_feed_format, 'encoding')
		settings[input_feed_format]['header_lines_number'] = self.ini_parser.get_param(input_feed_format, 'header_lines_number', 'int')
		settings[input_feed_format]['columns'] = self.tools.explode(',', self.ini_parser.get_param(input_feed_format, 'columns'))
		settings[input_feed_format]['column_separator'] = self.tools.escape_sequence(self.ini_parser.get_param(input_feed_format, 'column_separator'))
		settings[input_feed_format]['column_data_types'] = self.tools.explode(',', self.ini_parser.get_param(input_feed_format, 'column_data_types'))
		
		self.compare_elements_number(settings, input_feed_format, 'columns', input_feed_format, 'column_data_types')
		
	def set_params(self, args):
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
		self.settings['plotter']['x_ticks_data_columns'] = tools.explode(',', self.ini_parser.get_param('plotter', 'x_ticks_data_columns'))
		self.settings['plotter']['x_ticks'] = tools.explode(',', self.ini_parser.get_param('plotter', 'x_ticks'))
		self.settings['plotter']['x_labels_format'] = tools.explode(',', self.ini_parser.get_param('plotter', 'x_labels_format'))
		self.settings['plotter']['series'] = tools.explode(',', self.ini_parser.get_param('plotter', 'series'))
		self.settings['plotter']['subplot_height_share'] = tools.int_arr(tools.explode(',', self.ini_parser.get_param('plotter', 'subplot_height_share')))
		self.settings['plotter']['subplots_number'] = self.ini_parser.get_param('plotter', 'subplots_number', 'int') 
		self.settings['plotter']['seria_to_subbplot_binding'] = tools.int_arr(tools.explode(',', self.ini_parser.get_param('plotter', 'seria_to_subbplot_binding')))
		
		def clone_value(value, number):
			return number * [value]
		
		ignoring_missed_data_line = tools.implode(',', clone_value(self.ini_parser.get_param('plotter_default', 'ignoring_missed_data_line'), len(self.settings['plotter']['series'])))
		series_linewidth = tools.implode(',', clone_value(self.ini_parser.get_param('plotter_default', 'series_linewidth'), len(self.settings['plotter']['series'])))
		series_markersize = tools.implode(',', clone_value(self.ini_parser.get_param('plotter_default', 'series_markersize'), len(self.settings['plotter']['series'])))
		series_marker = tools.implode(',', clone_value(self.ini_parser.get_param('plotter_default', 'series_marker'), len(self.settings['plotter']['series'])))
		series_color = tools.implode(',', clone_value(self.ini_parser.get_param('plotter_default', 'series_color'), len(self.settings['plotter']['series'])))
		series_alpha = tools.implode(',', clone_value(self.ini_parser.get_param('plotter_default', 'series_alpha'), len(self.settings['plotter']['series'])))
		
		self.settings['plotter']['ignoring_missed_data_line'] = tools.bool_arr(tools.explode(',', self.ini_parser.get_param('plotter', 'ignoring_missed_data_line', error_ignoring = True, default_param_value = ignoring_missed_data_line)))
		self.settings['plotter']['series_linewidth'] = tools.int_arr(tools.explode(',', self.ini_parser.get_param('plotter', 'series_linewidth', error_ignoring = True, default_param_value = series_linewidth)))
		self.settings['plotter']['series_marker'] = tools.explode(',', self.ini_parser.get_param('plotter', 'series_marker', error_ignoring = True, default_param_value = series_marker))
		self.settings['plotter']['series_markersize'] = tools.int_arr(tools.explode(',', self.ini_parser.get_param('plotter', 'series_markersize', error_ignoring = True, default_param_value = series_markersize)))
		self.settings['plotter']['series_color'] = tools.explode(',', self.ini_parser.get_param('plotter', 'series_color', error_ignoring = True, default_param_value = series_color))
		self.settings['plotter']['series_alpha'] = tools.float_arr(tools.explode(',', self.ini_parser.get_param('plotter', 'series_alpha', error_ignoring = True, default_param_value = series_alpha)))
		
		#check several params
		def check_elements_number(section1, param1, section2, param2):
			if self.errors.error_occured:
				return None
			elements_number1 = len(self.settings[section1][param1])
			elements_number2 = self.settings[section2][param2]
			
			if elements_number1 != elements_number2:
				self.errors.raise_error('[' + section1 + '][' + param1 + '] elements number(' + str(elements_number1) + ') is not equal [' + section2 + '][' + param2 + '] value(' +  str(elements_number2) + ')')

		check_elements_number('plotter', 'subplot_height_share', 'plotter', 'subplots_number')
		
		def compare_elements_number(section1, param1, section2, param2):
			if self.errors.error_occured:
				return None
			elements_number1 = len(self.settings[section1][param1])
			elements_number2 = len(self.settings[section2][param2])
			if elements_number1 != elements_number2:
				self.errors.raise_error('[' + section1 + '][' + param1 + '] elements number(' + str(elements_number1) + ') is not equal [' + section2 + '][' + param2 + '] elements number(' +  str(elements_number2) + ')')

		compare_elements_number(input_feed_format, 'columns', input_feed_format, 'column_data_types')
		compare_elements_number('plotter', 'x_ticks_data_columns', 'plotter', 'x_ticks')
		compare_elements_number('plotter', 'x_ticks_data_columns', 'plotter', 'x_labels_format')
		compare_elements_number('plotter', 'series', 'plotter', 'seria_to_subbplot_binding')
		
	
