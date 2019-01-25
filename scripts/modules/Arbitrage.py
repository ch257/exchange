# -*- coding: utf-8 -*

from modules.common.Errors import *
from modules.common.FileSystem import *
from modules.common.SettingsReader import *
from modules.common.DataStream import *
# from modules.common.DataProccessing import *
# from modules.common.Plotter import *

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
			settings_reader.read_ArbitrageSettings(self.settings, ini_file_path, encoding)
			# settings_reader.read_PlotterSettings(self.settings, ini_file_path, encoding)
	
	def main(self, args):
		self.read_settings(args)
		# print(self.settings)
		
		fs = FileSystem(self.errors)
		data_stream = DataStream(self.errors)
		
		input_file_path = self.settings['input']['file_path']
		input_feed_format = self.settings[self.settings['input']['input_feed_format']]
		
		output_folder = self.settings['output']['folder']
		output_file = self.settings['output']['file']
		output_file_path = output_folder + output_file
		output_feed_format = self.settings[self.settings['output']['output_feed_format']]
		
		fs.create_folder_branch(output_folder)
		
		data_stream.open_stream(input_file_path, input_feed_format)
		data = data_stream.read_all(input_feed_format)
		data_stream.close_stream()
		
		output_feed_format['columns'].append('<EURUSD_R>')
		output_feed_format['column_data_types'].append('num')
		data['<EURUSD_R>'] = []
		rec = {}
		r = None
		rc = None
		for rec_cnt in range(len(data['<DATE>'])):
			close_1 = data['<CLOSE_1>'][rec_cnt]
			close_2 = data['<CLOSE_2>'][rec_cnt]
			if rec_cnt > 0:
				d_1 = close_1 - last_close_1
				d_2 = close_2 - last_close_2
				r = d_2 - d_1
				if rc != None:
					rc += last_r
				else:
					rc = r
				
			data['<EURUSD_R>'].append(rc)
			
			last_close_1 = close_1
			last_close_2 = close_2
			last_r = r
			
			
		data_stream.open_stream(output_file_path, output_feed_format, mode='w')
		data_stream.write_all(data, output_feed_format)
		data_stream.close_stream()
		
		# fig_name = '0000'
		# plotter = Plotter(self.errors)
		# plotter.plot_series(data, self.settings, fig_name)
		
		# print(data)
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')