# -*- coding: utf-8 -*

from modules.common.Errors import *
from modules.common.FileSystem import *
from modules.common.SettingsReader import *
from modules.common.DataStream import *
from modules.common.DataProccessing import *
from modules.common.DataIterator import *
from modules.common.Tools import *
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
		dp = DataProccessing(self.errors)
		tools = Tools(self.errors)
		
		input_file_path = self.settings['input']['file_path']
		input_feed_format = self.settings[self.settings['input']['input_feed_format']]
		
		moex_currency_file = self.settings['input']['moex_currency_file']
		moex_currency_feed_format = self.settings[self.settings['input']['moex_currency_feed_format']]
		
		output_folder = self.settings['output']['folder']
		output_file = self.settings['output']['file']
		output_file_path = output_folder + output_file
		output_feed_format = self.settings[self.settings['output']['output_feed_format']]
		
		fs.create_folder_branch(output_folder)
		
		data_stream.open_stream(input_file_path, input_feed_format)
		data = data_stream.read_all(input_feed_format)
		data_stream.close_stream()
		
		data_stream.open_stream(moex_currency_file, moex_currency_feed_format)
		moex_currency_data = data_stream.read_all(moex_currency_feed_format)
		data_stream.close_stream()
		
		time_range = dp.generate_time_range('12:00:00', '00:00:00', '00:05:00', tools.explode(',', '18:50:00-19:05:00'))
		date_range = dp.select_date_range(moex_currency_data['<DATE>'])
		moex_currency_timed_data = dp.create_data_by_time_range(time_range, date_range, moex_currency_data, ['<USDRUR>'])
		# print(moex_currency_timed_data['<DATE>'])
		
		dp.add_column('<USDRUR>', 'num', len(data['<DATE>']), data, output_feed_format)
		
		di_moex_timed_data = DataIterator(self.errors, moex_currency_timed_data, '<DATE>', moex_currency_feed_format)
		di_data = DataIterator(self.errors, data, '<DATE>', output_feed_format)
		last_USDRUR = None
		while not di_data.EOD:
			d_rec = di_data.get_next_rec()
			while not di_moex_timed_data.EOD:
				mtd_rec = di_moex_timed_data.get_next_rec()
				if mtd_rec['<USDRUR>'] != None:
					last_USDRUR = mtd_rec['<USDRUR>']
				if d_rec['<DATE>']['yyyymmdd'] > mtd_rec['<DATE>']:
					continue
				else:
					if d_rec['<DATE>']['yyyymmdd'] == mtd_rec['<DATE>'] and d_rec['<TIME>']['hhmmss'] > mtd_rec['<TIME>']:
						continue
					else:
						if d_rec['<DATE>']['yyyymmdd'] == mtd_rec['<DATE>']:
							data['<USDRUR>'][di_data.rec_cnt - 1] = last_USDRUR #mtd_rec['<USDRUR>']
							if d_rec['<TIME>']['hhmmss'] > mtd_rec['<TIME>']:
								di_moex_timed_data.rec_cnt -= 1
							break
						else:
							continue
							
		# print(data['<USDRUR>'])
		# print(len(data['<USDRUR>']))
		# print(len(data['<DATE>']))
		
		# di_data = DataIterator(self.errors, data, '<DATE>', output_feed_format)
		# while not di_data.EOD:
			# d_rec = di_data.get_next_rec()
			# print(d_rec['<DATE>']['yyyymmdd'] + ' ' + d_rec['<TIME>']['hhmmss'] + ' ' + str(d_rec['<USDRUR>']))
			
		
		dp.add_column('<Eu_RUR>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<ED_RUR>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<ED_Eu_RUR>', 'num', len(data['<DATE>']), data, output_feed_format)
		
		for rec_cnt in range(len(data['<DATE>'])):
			rec = dp.get_rec(rec_cnt, data, output_feed_format)
			Eu_C = rec['<Eu_C>']
			Si_C = rec['<Si_C>']
			ED_C = rec['<ED_C>']
			EURUSD_C = rec['<EURUSD_C>']
			USDRUR = rec['<USDRUR>']
			
			if rec_cnt > 0:
				Eu_RUR += Eu_C - last_Eu_C
				ED_RUR += (ED_C - last_ED_C) * USDRUR * 1000
				ED_Eu_RUR = ED_RUR - Eu_RUR
				# print(ED_RUR)
				
			else:
				Eu_RUR = 0
				ED_RUR = 0
				ED_Eu_RUR = 0

			last_Si_C = Si_C
			last_Eu_C = Eu_C
			last_ED_C = ED_C
			last_EURUSD_C = EURUSD_C

			data['<Eu_RUR>'][rec_cnt] = Eu_RUR
			data['<ED_RUR>'][rec_cnt] = ED_RUR
			data['<ED_Eu_RUR>'][rec_cnt] = ED_Eu_RUR
			
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