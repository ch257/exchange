# -*- coding: utf-8 -*

from modules.common.Errors import *
from modules.common.FileSystem import *
from modules.common.SettingsReader import *
from modules.common.DataStream import *
from modules.common.DataProccessing import *
from modules.common.DataIterator import *
from modules.common.Tools import *

from modules.indicators.SMA import *
# from modules.common.Plotter import *

class Arbitrage:
	def __init__(self):
		self.errors = Errors()
		self.settings = {}
		
		self.open_long = False
		self.open_short = False
		self.Eu_lots = 0
		self.Si_lots = 0
		self.ED_lots = 0
		self.Eu_op = 0
		self.Si_op = 0
		self.ED_op = 0
		self.deal_cnt = 0
		self.open_time = ''
		
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
	
	
	# N*Eu_RUR - (N+1)*Si_RUR - N*ED_RUR
	def openLong(self, rec, N):
		rec['<Si_open_long>'] = rec['<Si_C>']
		rec['<Eu_open_long>'] = rec['<Eu_C>']
		rec['<ED_open_long>'] = rec['<ED_C>'] * rec['<USDRUR>'] * 1000
		rec['<Si_lots>'] = (N+1)
		rec['<Eu_lots>'] = -N
		rec['<ED_lots>'] = N
		self.Si_lots = (N+1)
		self.Eu_lots = -N
		self.ED_lots = N
		self.Si_op = rec['<Si_C>']
		self.Eu_op = rec['<Eu_C>']
		self.ED_op = rec['<ED_C>']
		self.open_time = rec['<TIME>']['hhmmss']
		
	def closeLong(self, rec, N):
		rec['<Si_close_long>'] = rec['<Si_C>']
		rec['<Eu_close_long>'] = rec['<Eu_C>']
		rec['<ED_close_long>'] = rec['<ED_C>'] * rec['<USDRUR>'] * 1000
		rec['<Si_lots>'] = -(N+1)
		rec['<Eu_lots>'] = N
		rec['<ED_lots>'] = -N
		rec['<Eu_eqv>'] = self.Eu_op * self.Eu_lots + rec['<Eu_C>'] * rec['<Eu_lots>']
		rec['<Si_eqv>'] = self.Si_op * self.Si_lots + rec['<Si_C>'] * rec['<Si_lots>']
		rec['<ED_eqv>'] = (self.ED_op * self.ED_lots + rec['<ED_C>'] * rec['<ED_lots>']) * 1000 * rec['<USDRUR>']
		rec['<all_eqv>'] = rec['<Eu_eqv>'] + rec['<Si_eqv>'] + rec['<ED_eqv>']
		# self.Si_lots += -(N+1)
		# self.Eu_lots += N
		# self.ED_lots += -N
		# self.Si_op = rec['<Si_C>']
		# self.Eu_op = rec['<Eu_C>']
		# self.ED_op = rec['<ED_C>']
		self.deal_cnt += 1
		rec['<open_time>'] = self.open_time
		
	def openShort(self, rec, N):
		rec['<Si_open_short>'] = rec['<Si_C>']
		rec['<Eu_open_short>'] = rec['<Eu_C>']
		rec['<ED_open_short>'] = rec['<ED_C>'] * rec['<USDRUR>'] * 1000
		rec['<Si_lots>'] = -(N+1)
		rec['<Eu_lots>'] = N
		rec['<ED_lots>'] = -N
		self.Si_lots = -(N+1)
		self.Eu_lots = N
		self.ED_lots = -N
		self.Si_op = rec['<Si_C>']
		self.Eu_op = rec['<Eu_C>']
		self.ED_op = rec['<ED_C>']
		self.open_time = rec['<TIME>']['hhmmss']
		
	def closeShort(self, rec, N):
		rec['<Si_close_short>'] = rec['<Si_C>']
		rec['<Eu_close_short>'] = rec['<Eu_C>']
		rec['<ED_close_short>'] = rec['<ED_C>'] * rec['<USDRUR>'] * 1000
		rec['<Si_lots>'] = (N+1)
		rec['<Eu_lots>'] = -N
		rec['<ED_lots>'] = N
		rec['<Eu_eqv>'] = self.Eu_op * self.Eu_lots + rec['<Eu_C>'] * rec['<Eu_lots>']
		rec['<Si_eqv>'] = self.Si_op * self.Si_lots + rec['<Si_C>'] * rec['<Si_lots>']
		rec['<ED_eqv>'] = (self.ED_op * self.ED_lots + rec['<ED_C>'] * rec['<ED_lots>']) * 1000 * rec['<USDRUR>']
		rec['<all_eqv>'] = rec['<Eu_eqv>'] + rec['<Si_eqv>'] + rec['<ED_eqv>']
		# self.Si_lots += (N+1)
		# self.Eu_lots += -N
		# self.ED_lots += N
		# self.Si_op = rec['<Si_C>']
		# self.Eu_op = rec['<Eu_C>']
		# self.ED_op = rec['<ED_C>']
		self.deal_cnt += 1
		rec['<open_time>'] = self.open_time
	
	def traiding(self, gamma, gamma_avg, rec, N):
		if gamma_avg != None:	
			delta = gamma - gamma_avg
			dev = 100
			buy_signal = False
			sell_signal = False
			if delta < -dev:
				buy_signal = True
			if delta > dev:
				sell_signal = True
			
			################################	
			if self.open_long:
				if delta >= 0:
					self.open_long = False
					self.closeLong(rec, N)
			elif self.open_short:
				if delta <= 0:
					self.open_short = False
					self.closeShort(rec, N)
					
			#143500 152500; 154500 165500; 193500 202500
			elif not (self.open_long or self.open_short):
				t = rec['<TIME>']['hhmmss']
				if sell_signal:
					if ('143500' <= t and t < '152500' or
						'154500' <= t and t < '165500' or
						'193500' <= t and t < '202500'):
						self.openShort(rec, N)
						self.open_short = True
				elif buy_signal:
					if ('143500' <= t and t < '152500' or
						'154500' <= t and t < '165500' or
						'193500' <= t and t < '202500'):
						self.openLong(rec, N)
						self.open_long = True
	
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
		# print(moex_currency_timed_data['<USDRUR>'])
		
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
			
		
		dp.add_column('<Si_RUR>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Eu_RUR>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<ED_RUR>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<gamma>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<gamma_avg>', 'num', len(data['<DATE>']), data, output_feed_format)
		
		dp.add_column('<Si_open_long>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Si_open_short>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Si_lots>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Si_close_long>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Si_close_short>', 'num', len(data['<DATE>']), data, output_feed_format)

		dp.add_column('<Eu_open_long>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Eu_open_short>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Eu_lots>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Eu_close_long>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Eu_close_short>', 'num', len(data['<DATE>']), data, output_feed_format)

		dp.add_column('<ED_open_long>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<ED_open_short>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<ED_lots>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<ED_close_long>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<ED_close_short>', 'num', len(data['<DATE>']), data, output_feed_format)
		
		dp.add_column('<Eu_eqv>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<Si_eqv>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<ED_eqv>', 'num', len(data['<DATE>']), data, output_feed_format)
		dp.add_column('<open_time>', 'str', len(data['<DATE>']), data, output_feed_format)
		
		dp.add_column('<all_eqv>', 'num', len(data['<DATE>']), data, output_feed_format)
		
		
		avg_per = 21
		sma = SMA(avg_per)
		N = 7
		for rec_cnt in range(len(data['<DATE>'])):
			rec = dp.get_rec(rec_cnt, data, output_feed_format)
			Si_C = rec['<Si_C>']
			Eu_C = rec['<Eu_C>']
			ED_C = rec['<ED_C>']
			USDRUR = rec['<USDRUR>']
			
			if rec_cnt > 0:
				Si_RUR += Si_C - last_Si_C
				Eu_RUR += Eu_C - last_Eu_C
				ED_RUR += (ED_C - last_ED_C) * Si_C #USDRUR * 1000
				gamma = (Eu_RUR - Si_RUR - ED_RUR) * N - Si_RUR  # N*Eu_RUR - (N+1)*Si_RUR - N*ED_RUR
				gamma_avg = sma.calc(gamma)
				
				self.traiding(gamma, gamma_avg, rec, N)
				# print(ED_RUR)
				
			else:
				Si_RUR = 0
				Eu_RUR = 0
				ED_RUR = 0
				gamma = 0
				gamma_avg = None

			last_Si_C = Si_C
			last_Eu_C = Eu_C
			last_ED_C = ED_C
			
			data['<Si_RUR>'][rec_cnt] = Si_RUR
			data['<Eu_RUR>'][rec_cnt] = Eu_RUR
			data['<ED_RUR>'][rec_cnt] = ED_RUR
			data['<gamma>'][rec_cnt] = gamma
			data['<gamma_avg>'][rec_cnt] = gamma_avg
			
			data['<Si_open_long>'][rec_cnt] = rec['<Si_open_long>']
			data['<Si_open_short>'][rec_cnt] = rec['<Si_open_short>']
			data['<Si_lots>'][rec_cnt] = rec['<Si_lots>']
			data['<Si_close_long>'][rec_cnt] = rec['<Si_close_long>']
			data['<Si_close_short>'][rec_cnt] = rec['<Si_close_short>']
			
			data['<Eu_open_long>'][rec_cnt] = rec['<Eu_open_long>']
			data['<Eu_open_short>'][rec_cnt] = rec['<Eu_open_short>']
			data['<Eu_lots>'][rec_cnt] = rec['<Eu_lots>']
			data['<Eu_close_long>'][rec_cnt] = rec['<Eu_close_long>']
			data['<Eu_close_short>'][rec_cnt] = rec['<Eu_close_short>']
			
			data['<ED_open_long>'][rec_cnt] = rec['<ED_open_long>']
			data['<ED_open_short>'][rec_cnt] = rec['<ED_open_short>']
			data['<ED_lots>'][rec_cnt] = rec['<ED_lots>']
			data['<ED_close_long>'][rec_cnt] = rec['<ED_close_long>']
			data['<ED_close_short>'][rec_cnt] = rec['<ED_close_short>']
			
			data['<Eu_eqv>'][rec_cnt] = rec['<Eu_eqv>']
			data['<Si_eqv>'][rec_cnt] = rec['<Si_eqv>']
			data['<ED_eqv>'][rec_cnt] = rec['<ED_eqv>']
			data['<open_time>'][rec_cnt] = rec['<open_time>']
			
			data['<all_eqv>'][rec_cnt] = rec['<all_eqv>']
			
		data_stream.open_stream(output_file_path, output_feed_format, mode='w')
		data_stream.write_all(data, output_feed_format)
		data_stream.close_stream()
		
		# fig_name = '0000'
		# plotter = Plotter(self.errors)
		# plotter.plot_series(data, self.settings, fig_name)
		
		print(self.deal_cnt)
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')