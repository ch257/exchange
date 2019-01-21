# -*- coding: utf-8 -*

from modules.common.Errors import *
from modules.common.SettingsReader import *
# from modules.common.Tools import *
from modules.common.DataStream import *
from modules.common.DataProccessing import *
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
			settings_reader.read_DataStraemSettings(self.settings, ini_file_path, encoding)
			# settings_reader.read_PlotterSettings(self.settings, ini_file_path, encoding)
	
	def main(self, args):
		self.read_settings(args)
		# print(self.settings)
		
		data_stream = DataStream(self.errors)
		si_input_file_path = self.settings['input']['si_file_path']
		eu_input_file_path = self.settings['input']['eu_file_path']
		eurusd_input_file_path = self.settings['input']['eurusd_file_path']
		input_feed_format = self.settings[self.settings['input']['input_feed_format']]
		
		data_stream.open_stream(si_input_file_path, input_feed_format)
		si_data = data_stream.read_all(input_feed_format)
		data_stream.close_stream()

		data_stream.open_stream(eu_input_file_path, input_feed_format)
		eu_data = data_stream.read_all(input_feed_format)
		data_stream.close_stream()

		data_stream.open_stream(eurusd_input_file_path, input_feed_format)
		eurusd_data = data_stream.read_all(input_feed_format)
		data_stream.close_stream()
		# print(eurusd_data)
		
		dp = DataProccessing(self.errors)
		
		start = '12:00:00'
		stop = '00:00:00'
		step = '00:05:00'
		exclude = [
			['18:50:00', '19:05:00']
		]
		time_range = dp.generate_time_range(start, stop, step, exclude)
		columns = ['<CLOSE>']
		
		date_range = dp.select_date_range(si_data['<DATE>'])
		
		si_timed_data = dp.create_data_by_time_range(time_range, date_range, si_data, columns)
		# print(si_timed_data)
		
		eu_timed_data = dp.create_data_by_time_range(time_range, date_range, eu_data, columns)
		# print(eu_timed_data)
		
		eurusd_timed_data = dp.create_data_by_time_range(time_range, date_range, eurusd_data, columns)
		# print(eurusd_timed_data)
		
		all_data = {}
		all_data['<DATE>'] = si_timed_data['<DATE>']
		all_data['<TIME>'] = si_timed_data['<TIME>']
		all_data['<siCLOSE>'] = si_timed_data['<CLOSE>']
		all_data['<euCLOSE>'] = eu_timed_data['<CLOSE>']
		all_data['<eurusdCLOSE>'] = eurusd_timed_data['<CLOSE>']
		
		# print(all_data['<DATE>'])
		
		content = ''
		for cnt in range(len(all_data['<DATE>'])):
			content += (
				all_data['<DATE>'][cnt] + '\t' + 
				all_data['<TIME>'][cnt] + '\t' + 
				str(all_data['<siCLOSE>'][cnt]) + '\t' + 
				str(all_data['<euCLOSE>'][cnt]) + '\t' + 
				str(all_data['<eurusdCLOSE>'][cnt]) + '\n')
		
		try:
			with open('data/output/arb.txt', "w") as text_file:
				print(content, file=text_file)
		except Exception as e:
			self.errors.raise_error('Can\'t write file ' + 'data/output/arb.txt')
		
		
		# fig_name = '0000'
		# plotter = Plotter(self.errors)
		# plotter.plot_series(data, self.settings, fig_name)
		
		# print(data)
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')