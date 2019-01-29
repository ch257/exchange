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
		
	def check_elements_number(self, settings, section1, param1, section2, param2):
		elements_number1 = len(settings[section1][param1])
		elements_number2 = settings[section2][param2]
		
		if elements_number1 != elements_number2:
			self.errors.raise_error('[' + section1 + '][' + param1 + '] elements number(' + str(elements_number1) + ') is not equal [' + section2 + '][' + param2 + '] value(' +  str(elements_number2) + ')')
	
	def compare_elements_number(self, settings, section1, param1, section2, param2):
		elements_number1 = len(settings[section1][param1])
		elements_number2 = len(settings[section2][param2])
		if elements_number1 != elements_number2:
			self.errors.raise_error('[' + section1 + '][' + param1 + '] elements number(' + str(elements_number1) + ') is not equal [' + section2 + '][' + param2 + '] elements number(' +  str(elements_number2) + ')')
		
	def clone_value(self, value, number):
		return number * [value]
	
	def read_ArbitrageSettings(self, settings, ini_file_path, encoding):
		if self.errors.error_occured:
			return None
		
		self.ini_parser.read_ini(ini_file_path, encoding)
		settings['input'] = {}
		settings['input']['file_path'] = self.ini_parser.get_param('input', 'file_path')
		settings['input']['input_feed_format'] = self.ini_parser.get_param('input', 'input_feed_format')
		settings['input']['moex_currency_file'] = self.ini_parser.get_param('input', 'moex_currency_file')
		settings['input']['moex_currency_feed_format'] = self.ini_parser.get_param('input', 'moex_currency_feed_format')

		settings['output'] = {}
		settings['output']['folder'] = self.ini_parser.get_param('output', 'folder')
		settings['output']['file'] = self.ini_parser.get_param('output', 'file')
		settings['output']['output_feed_format'] = self.ini_parser.get_param('output', 'output_feed_format')
		
		input_feed_format = settings['input']['input_feed_format']
		settings[input_feed_format] = {}
		settings[input_feed_format]['encoding'] = self.ini_parser.get_param(input_feed_format, 'encoding')
		settings[input_feed_format]['header_lines_number'] = self.ini_parser.get_param(input_feed_format, 'header_lines_number', 'int')
		settings[input_feed_format]['columns'] = self.tools.explode(',', self.ini_parser.get_param(input_feed_format, 'columns'))
		settings[input_feed_format]['column_separator'] = self.tools.escape_sequence(self.ini_parser.get_param(input_feed_format, 'column_separator'))
		settings[input_feed_format]['column_data_types'] = self.tools.explode(',', self.ini_parser.get_param(input_feed_format, 'column_data_types'))
		
		moex_currency_feed_format = settings['input']['moex_currency_feed_format']
		settings[moex_currency_feed_format] = {}
		settings[moex_currency_feed_format]['encoding'] = self.ini_parser.get_param(moex_currency_feed_format, 'encoding')
		settings[moex_currency_feed_format]['header_lines_number'] = self.ini_parser.get_param(moex_currency_feed_format, 'header_lines_number', 'int')
		settings[moex_currency_feed_format]['columns'] = self.tools.explode(',', self.ini_parser.get_param(moex_currency_feed_format, 'columns'))
		settings[moex_currency_feed_format]['column_separator'] = self.tools.escape_sequence(self.ini_parser.get_param(moex_currency_feed_format, 'column_separator'))
		settings[moex_currency_feed_format]['column_data_types'] = self.tools.explode(',', self.ini_parser.get_param(moex_currency_feed_format, 'column_data_types'))
		
		output_feed_format = settings['output']['output_feed_format']
		settings[output_feed_format] = {}
		settings[output_feed_format]['encoding'] = self.ini_parser.get_param(output_feed_format, 'encoding')
		settings[output_feed_format]['header_lines_number'] = self.ini_parser.get_param(output_feed_format, 'header_lines_number', 'int')
		settings[output_feed_format]['columns'] = self.tools.explode(',', self.ini_parser.get_param(output_feed_format, 'columns'))
		settings[output_feed_format]['column_separator'] = self.tools.escape_sequence(self.ini_parser.get_param(output_feed_format, 'column_separator'))
		settings[output_feed_format]['column_data_types'] = self.tools.explode(',', self.ini_parser.get_param(output_feed_format, 'column_data_types'))
		
		#check several params
		self.compare_elements_number(settings, input_feed_format, 'columns', input_feed_format, 'column_data_types')
		self.compare_elements_number(settings, moex_currency_feed_format, 'columns', moex_currency_feed_format, 'column_data_types')
		self.compare_elements_number(settings, output_feed_format, 'columns', output_feed_format, 'column_data_types')
		
	def read_JoinData_settings(self, settings, ini_file_path, encoding):
		if self.errors.error_occured:
			return None
		
		self.ini_parser.read_ini(ini_file_path, encoding)
		settings['input'] = {}
		settings['input']['folder'] = self.ini_parser.get_param('input', 'folder')
		settings['input']['input_feed_format'] = self.ini_parser.get_param('input', 'input_feed_format')
		settings['input']['columns'] = self.tools.explode(',', self.ini_parser.get_param('input', 'columns'))
		settings['input']['column_data_types'] = self.tools.explode(',', self.ini_parser.get_param('input', 'column_data_types'))
		
		settings['input']['date_col'] = self.ini_parser.get_param('input', 'date_col')
		settings['input']['start_time'] = self.ini_parser.get_param('input', 'start_time')
		settings['input']['stop_time'] = self.ini_parser.get_param('input', 'stop_time')
		settings['input']['step_time'] = self.ini_parser.get_param('input', 'step_time')
		settings['input']['exclude_time'] = self.tools.explode(',', self.ini_parser.get_param('input', 'exclude_time'))
		
		settings['output'] = {}
		settings['output']['folder'] = self.ini_parser.get_param('output', 'folder')
		settings['output']['file'] = self.ini_parser.get_param('output', 'file')
		settings['output']['output_feed_format'] = self.ini_parser.get_param('output', 'output_feed_format')
		
		input_feed_format = settings['input']['input_feed_format']
		settings[input_feed_format] = {}
		settings[input_feed_format]['encoding'] = self.ini_parser.get_param(input_feed_format, 'encoding')
		settings[input_feed_format]['header_lines_number'] = self.ini_parser.get_param(input_feed_format, 'header_lines_number', 'int')
		settings[input_feed_format]['columns'] = self.tools.explode(',', self.ini_parser.get_param(input_feed_format, 'columns'))
		settings[input_feed_format]['column_separator'] = self.tools.escape_sequence(self.ini_parser.get_param(input_feed_format, 'column_separator'))
		settings[input_feed_format]['column_data_types'] = self.tools.explode(',', self.ini_parser.get_param(input_feed_format, 'column_data_types'))
		
		output_feed_format = settings['output']['output_feed_format']
		settings[output_feed_format] = {}
		settings[output_feed_format]['encoding'] = self.ini_parser.get_param(output_feed_format, 'encoding')
		settings[output_feed_format]['header_lines_number'] = self.ini_parser.get_param(output_feed_format, 'header_lines_number', 'int')
		# settings[output_feed_format]['columns'] = self.tools.explode(',', self.ini_parser.get_param(output_feed_format, 'columns'))
		settings[output_feed_format]['column_separator'] = self.tools.escape_sequence(self.ini_parser.get_param(output_feed_format, 'column_separator'))
		# settings[output_feed_format]['column_data_types'] = self.tools.explode(',', self.ini_parser.get_param(output_feed_format, 'column_data_types'))
		
		#check several params
		self.compare_elements_number(settings, input_feed_format, 'columns', input_feed_format, 'column_data_types')
		# self.compare_elements_number(settings, output_feed_format, 'columns', output_feed_format, 'column_data_types')
		self.compare_elements_number(settings, 'input', 'columns', 'input', 'column_data_types')
		
	
	def read_ConcatinateData_settings(self, settings, ini_file_path, encoding):
		if self.errors.error_occured:
			return None
		
		self.ini_parser.read_ini(ini_file_path, encoding)
		settings['input'] = {}
		settings['input']['folder'] = self.ini_parser.get_param('input', 'folder')
		settings['input']['input_feed_format'] = self.ini_parser.get_param('input', 'input_feed_format')
		
		settings['output'] = {}
		settings['output']['folder'] = self.ini_parser.get_param('output', 'folder')
		settings['output']['file'] = self.ini_parser.get_param('output', 'file')
		settings['output']['output_feed_format'] = self.ini_parser.get_param('output', 'output_feed_format')
		
		input_feed_format = settings['input']['input_feed_format']
		settings[input_feed_format] = {}
		settings[input_feed_format]['encoding'] = self.ini_parser.get_param(input_feed_format, 'encoding')
		settings[input_feed_format]['header_lines_number'] = self.ini_parser.get_param(input_feed_format, 'header_lines_number', 'int')
		settings[input_feed_format]['columns'] = self.tools.explode(',', self.ini_parser.get_param(input_feed_format, 'columns'))
		settings[input_feed_format]['column_separator'] = self.tools.escape_sequence(self.ini_parser.get_param(input_feed_format, 'column_separator'))
		settings[input_feed_format]['column_data_types'] = self.tools.explode(',', self.ini_parser.get_param(input_feed_format, 'column_data_types'))
		
		output_feed_format = settings['output']['output_feed_format']
		settings[output_feed_format] = {}
		settings[output_feed_format]['encoding'] = self.ini_parser.get_param(output_feed_format, 'encoding')
		settings[output_feed_format]['header_lines_number'] = self.ini_parser.get_param(output_feed_format, 'header_lines_number', 'int')
		settings[output_feed_format]['columns'] = self.tools.explode(',', self.ini_parser.get_param(output_feed_format, 'columns'))
		settings[output_feed_format]['column_separator'] = self.tools.escape_sequence(self.ini_parser.get_param(output_feed_format, 'column_separator'))
		settings[output_feed_format]['column_data_types'] = self.tools.explode(',', self.ini_parser.get_param(output_feed_format, 'column_data_types'))
		
		#check several params
		self.compare_elements_number(settings, input_feed_format, 'columns', input_feed_format, 'column_data_types')
		self.compare_elements_number(settings, output_feed_format, 'columns', output_feed_format, 'column_data_types')
		
	def read_PlotterSettings(self, settings, ini_file_path, encoding):
		if self.errors.error_occured:
			return None
			
		settings['output'] = {}
		settings['output']['folder'] = self.ini_parser.get_param('output', 'folder')
			
		settings['plotter'] = {}
		settings['plotter']['fig_folder'] = settings['output']['folder'] + self.ini_parser.get_param('plotter', 'fig_folder')
		settings['plotter']['x_ticks_data_columns'] = self.tools.explode(',', self.ini_parser.get_param('plotter', 'x_ticks_data_columns'))
		settings['plotter']['x_ticks'] = self.tools.explode(',', self.ini_parser.get_param('plotter', 'x_ticks'))
		settings['plotter']['x_labels_format'] = self.tools.explode(',', self.ini_parser.get_param('plotter', 'x_labels_format'))
		settings['plotter']['series'] = self.tools.explode(',', self.ini_parser.get_param('plotter', 'series'))
		settings['plotter']['subplot_height_share'] = self.tools.int_arr(self.tools.explode(',', self.ini_parser.get_param('plotter', 'subplot_height_share')))
		settings['plotter']['subplots_number'] = self.ini_parser.get_param('plotter', 'subplots_number', 'int') 
		settings['plotter']['seria_to_subbplot_binding'] = self.tools.int_arr(self.tools.explode(',', self.ini_parser.get_param('plotter', 'seria_to_subbplot_binding')))
		
		ignoring_missed_data_line = self.tools.implode(',', self.clone_value(self.ini_parser.get_param('plotter_default', 'ignoring_missed_data_line'), len(settings['plotter']['series'])))
		series_linewidth = self.tools.implode(',', self.clone_value(self.ini_parser.get_param('plotter_default', 'series_linewidth'), len(settings['plotter']['series'])))
		series_markersize = self.tools.implode(',', self.clone_value(self.ini_parser.get_param('plotter_default', 'series_markersize'), len(settings['plotter']['series'])))
		series_marker = self.tools.implode(',', self.clone_value(self.ini_parser.get_param('plotter_default', 'series_marker'), len(settings['plotter']['series'])))
		series_color = self.tools.implode(',', self.clone_value(self.ini_parser.get_param('plotter_default', 'series_color'), len(settings['plotter']['series'])))
		series_alpha = self.tools.implode(',', self.clone_value(self.ini_parser.get_param('plotter_default', 'series_alpha'), len(settings['plotter']['series'])))
		
		settings['plotter']['ignoring_missed_data_line'] = self.tools.bool_arr(self.tools.explode(',', self.ini_parser.get_param('plotter', 'ignoring_missed_data_line', error_ignoring = True, default_param_value = ignoring_missed_data_line)))
		settings['plotter']['series_linewidth'] = self.tools.int_arr(self.tools.explode(',', self.ini_parser.get_param('plotter', 'series_linewidth', error_ignoring = True, default_param_value = series_linewidth)))
		settings['plotter']['series_marker'] = self.tools.explode(',', self.ini_parser.get_param('plotter', 'series_marker', error_ignoring = True, default_param_value = series_marker))
		settings['plotter']['series_markersize'] = self.tools.int_arr(self.tools.explode(',', self.ini_parser.get_param('plotter', 'series_markersize', error_ignoring = True, default_param_value = series_markersize)))
		settings['plotter']['series_color'] = self.tools.explode(',', self.ini_parser.get_param('plotter', 'series_color', error_ignoring = True, default_param_value = series_color))
		settings['plotter']['series_alpha'] = self.tools.float_arr(self.tools.explode(',', self.ini_parser.get_param('plotter', 'series_alpha', error_ignoring = True, default_param_value = series_alpha)))
		
		#check several params
		self.check_elements_number(settings, 'plotter', 'subplot_height_share', 'plotter', 'subplots_number')
		self.compare_elements_number(settings, 'plotter', 'x_ticks_data_columns', 'plotter', 'x_ticks')
		self.compare_elements_number(settings, 'plotter', 'x_ticks_data_columns', 'plotter', 'x_labels_format')
		self.compare_elements_number(settings, 'plotter', 'series', 'plotter', 'seria_to_subbplot_binding')

