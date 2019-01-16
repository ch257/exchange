# -*- coding: utf-8 -*

import time
import datetime
from datetime import datetime as dt, date #, time
import urllib.request

from modules.common.Errors import *
from modules.common.IniParser import *
from modules.common.Tools import *
from modules.common.FileSystem import *

# import urllib.request
# url = 'http://export.finam.ru/SPFB.Eu-3.19_190108_190108.txt?market=14&em=487593&code=SPFB.Eu-3.19&apply=0&df=8&mf=0&yf=2019&from=08.01.2019&dt=8&mt=0&yt=2019&to=08.01.2019&p=3&f=SPFB.Eu-3.19_190108_190108&e=.txt&cn=SPFB.Eu-3.19&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'
# page = urllib.request.urlopen(url)
# content = page.read()
# print(content)


class GetFinamData:
	def __init__(self):
		self.errors = Errors()
		self.ini_encoding = 'utf-8'
		self.ini_parser = IniParser(self.errors)
		self.tc_ini_parser = IniParser(self.errors)
		self.settings = {}
	
	def read_settings(self, args):
		if len(args) < 2:
			self.errors.raise_error('no ini file path')
		else:
			encoding = self.ini_encoding
			if len(args) > 2:
				self.ini_encoding = args[2]
				
			ini_file_path = args[1]
			self.ini_parser.read_ini(args[1], self.ini_encoding)
	
	def set_params(self, args):
		tools = Tools(self.errors)
		self.read_settings(args)
		self.settings['common'] = {}
		self.settings['common']['time_frames'] = tools.explode(',', self.ini_parser.get_param('common', 'time_frames'))
		self.settings['common']['output_folder'] = self.ini_parser.get_param('common', 'output_folder')
		self.settings['common']['trading_calendar'] = self.ini_parser.get_param('common', 'trading_calendar')
		self.settings['common']['always_update_past_days_number'] = self.ini_parser.get_param('common', 'always_update_past_days_number', 'int')
		
		self.tc_ini_parser.read_ini(self.settings['common']['trading_calendar'], self.ini_encoding)
		# self.settings['non_working_days'] = {}
		# self.settings['non_working_days'] = self.tc_ini_parser.get_param('non_working_days')
		
		self.settings['contracts'] = {}
		tickers = tools.explode(',', self.ini_parser.get_param('contracts', 'tickers'))
		
		for ticker_idx in range(len(tickers)):	
			self.settings['contracts'][ticker_idx] = {}
			self.settings['contracts'][ticker_idx]['ticker'] = tickers[ticker_idx]
			self.settings['contracts'][ticker_idx]['list'] = {}
			list = tools.explode(',', self.ini_parser.get_param('contracts', tickers[ticker_idx]))
			for contract_idx in range(len(list)): 
				self.settings['contracts'][ticker_idx]['list'][contract_idx] = self.ini_parser.get_param(list[contract_idx])
			
	
	def get_contract(self, _idx = [0, 0]):
		if self.errors.error_occured:
			return None, None, None, None, None, None
		
		if _idx[0] < len(self.settings['contracts']):
			if _idx[1] < len(self.settings['contracts'][_idx[0]]['list']):
				Ticker = self.settings['contracts'][_idx[0]]['ticker']
				ContractSymbol = self.settings['contracts'][_idx[0]]['list'][_idx[1]]['ContractSymbol']
				ContractTradingSymbol = self.settings['contracts'][_idx[0]]['list'][_idx[1]]['ContractTradingSymbol']
				FirstTradingDay = self.settings['contracts'][_idx[0]]['list'][_idx[1]]['FirstTradingDay']
				LastTradingDay = self.settings['contracts'][_idx[0]]['list'][_idx[1]]['LastTradingDay']
				FinamEm = self.settings['contracts'][_idx[0]]['list'][_idx[1]]['FinamEm']
				_idx[1] += 1
			else:
				_idx[0] += 1
				_idx[1] = 0
				Ticker, ContractSymbol, ContractTradingSymbol, FirstTradingDay, LastTradingDay, FinamEm = self.get_contract(_idx)
		else:
			return None, None, None, None, None, None
		
		return Ticker, ContractSymbol, ContractTradingSymbol, FirstTradingDay, LastTradingDay, FinamEm
	
	def shape_finam_url(self, current_trading_day, arch, FinamEm, ContractSymbol, time_frame):
		# url = http://export.finam.ru/SPFB.Eu-3.19_190108_190108.txt?
		# market = 14 # Номер рынка
		# em = 487593 # Номер инструмента
		# code = SPFB.Eu-3.19 # Тикер инструмента
		# apply = 0 # 
		# df = 8 # Начальная дата, номер дня (1-31)
		# mf = 0 # Начальная дата, номер месяца (0-11)
		# yf = 2019 # Начальная дата, год
		# from = 08.01.2019 # Начальная дата
		# dt = 8 # Конечная дата, номер дня
		# mt = 0 # Конечная дата, номер месяца
		# yt = 2019 # Конечная дата, год
		# to = 08.01.2019 # Конечная дата
		# p = 3 # Таймфрейм {'tick': 1, 'min': 2, '5min': 3, '10min': 4, '15min': 5, '30min': 6, 'hour': 7, 'daily': 8, 'week': 9, 'month': 10}
		# f = SPFB.Eu-3.19_190108_190108 # Имя сформированного файла
		# e = .txt # Расширение сформированного файла#  возможны варианты — .txt либо .csv
		# cn = SPFB.Eu-3.19 # Имя контракта
		# dtf = 1 # формат даты (1 — ггггммдд, 2 — ггммдд, 3 — ддммгг, 4 — дд/мм/гг, 5 — мм/дд/гг)
		# tmf = 1 # формат времени (1 — ччммсс, 2 — ччмм, 3 — чч: мм: сс, 4 — чч: мм)
		# MSOR = 1 # выдавать время (0 — начала свечи, 1 — окончания свечи)
		# mstime = on # выдавать время (НЕ московское — mstimever=0#  московское — mstime='on', mstimever='1')
		# mstimever = 1 # Коррекция часового пояса
		# sep = 1 # Разделитель полей (1 — запятая (,), 2 — точка (.), 3 — точка с запятой (;), 4 — табуляция (»), 5 — пробел ( ))
		# sep2 = 1 # Разделитель разрядов (1 — нет, 2 — точка (.), 3 — запятая (,), 4 — пробел ( ), 5 — кавычка ('))
		# datf = 1 # Перечень получаемых данных (#1 — TICKER, PER, DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL#  #2 — TICKER, PER, DATE, TIME, OPEN, HIGH, LOW, CLOSE#  #3 — TICKER, PER, DATE, TIME, CLOSE, VOL#  #4 — TICKER, PER, DATE, TIME, CLOSE#  #5 — DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL#  #6 — DATE, TIME, LAST, VOL, ID, OPER).
		# at = 1 # добавлять заголовок в файл (0 — нет, 1 — да)
		
		url = 'http://export.finam.ru/'
		if arch:
			market = '13'
		else:
			market = '14'
		em = FinamEm
		code = 'SPFB.' + ContractSymbol
		apply = '0'
		df = str(current_trading_day.day)
		mf = str(current_trading_day.month - 1)
		yf = str(current_trading_day.year)
		_from = dt.strftime(current_trading_day, '%d.%m.%Y')
		_dt = str(current_trading_day.day)
		mt = str(current_trading_day.month - 1)
		yt = str(current_trading_day.year)
		to = dt.strftime(current_trading_day, '%d.%m.%Y')
		time_frame_codes = {'0': '1', '1': '2', '5': '3', '10': '4', '15': '5', '30': '6', '60': '7', 'D': '8', 'W': '9', 'M': '10'}
		p = time_frame_codes[time_frame]
		f = code + '_' + dt.strftime(current_trading_day, '%Y-%m-%d')
		e = '.txt'
		cn = code
		dtf = '1'
		tmf = '1'
		MSOR = '1'
		mstime = 'on' 
		mstimever = '1' 
		sep = '1'
		sep2 = '1'
		datf = '1'
		at = '1'
		
		url += (
			f + e + 
			'?market=' + market +
			'&em=' + em +
			'&code=' + code +
			'&apply=' + apply +
			'&df=' + df +
			'&mf=' + mf +
			'&yf=' + yf +
			'&from=' + _from +
			'&dt=' + _dt +
			'&mt=' + mt +
			'&yt=' + yt +
			'&to=' + to +
			'&p=' + p +
			'&f=' + f +
			'&e=' + e +
			'&cn=' + cn +
			'&dtf=' + dtf +
			'&tmf=' + tmf +
			'&MSOR=' + MSOR +
			'&mstime=' + mstime +
			'&mstimever=' + mstimever +
			'&sep=' + sep +
			'&sep2=' + sep2 +
			'&datf=' + datf +
			'&at=' + at +
		'')
			
		return url, f + e
	
	def is_non_working_day(self, current_trading_day):
		ctd_year = str(current_trading_day.year)
		ctd_month = str(current_trading_day.month)
		ctd_day = str(current_trading_day.day)

		tools = Tools(self.errors)
		nw_days =  tools.explode(',', self.tc_ini_parser.get_param('non_working_days', ctd_month + '.' + ctd_year))
		if ctd_day in nw_days:
			return True

		return False;
		
	def allow_update(self, now_day, current_trading_day, file_path) :
		if self.errors.error_occured:
			return False
		
		day_cnt = 1
		always_update_past_days_number = self.settings['common']['always_update_past_days_number']
		while always_update_past_days_number > 0:
			days_shift = datetime.timedelta(days=day_cnt)
			if not self.is_non_working_day(now_day - days_shift):
				always_update_past_days_number -= 1
			day_cnt += 1

		if current_trading_day < now_day - days_shift:
			if not self.is_non_working_day(current_trading_day):
				if not os.path.exists(file_path):
					return True
		elif current_trading_day <= now_day:
			if not self.is_non_working_day(current_trading_day):
				return True
		return False
	
	def main(self, args):
		self.set_params(args)
		
		fs = FileSystem(self.errors)
		now_day = dt.today().date()
		
		time_frames = self.settings['common']['time_frames']
				
		while not self.errors.error_occured:
			Ticker, ContractSymbol, ContractTradingSymbol, FirstTradingDay, LastTradingDay, FinamEm = self.get_contract()
			if Ticker:
				first_trading_day = dt.strptime(FirstTradingDay, '%d.%m.%Y').date()
				last_trading_day = dt.strptime(LastTradingDay, '%d.%m.%Y').date()
				ltd_year = last_trading_day.year
				
				# delta = last_trading_day - first_trading_day
				one_day = datetime.timedelta(days=1)
				current_trading_day = first_trading_day
				while not self.errors.error_occured:
				# for day_cnt in range(delta.days):
					for time_frame in time_frames:	
						if now_day > last_trading_day:
							arch = True
						else:
							arch = False
						path = self.settings['common']['output_folder'] + str(ltd_year) + '/' + Ticker + '/' + ContractSymbol + '/' + time_frame + '/'
						fs.create_folder_branch(path)
						url, file = self.shape_finam_url(current_trading_day, arch, FinamEm, ContractSymbol, time_frame)
						file_path = path + file		
						if self.allow_update(now_day, current_trading_day, file_path):
							print(Ticker, ContractSymbol, current_trading_day, time_frame)
							try:
								page = urllib.request.urlopen(url)
							except Exception as e:
								self.errors.raise_error('Can\'t open url ' + url)
								break
							content = page.read()
							content = content.decode('utf-8').replace('\r', '')
							
							try:
								with open(file_path, "w") as text_file:
									print(content, file=text_file)
							except Exception as e:
								self.errors.raise_error('Can\'t write file ' + file_path)
								break
							time.sleep(1)

					current_trading_day += one_day
					if current_trading_day > last_trading_day:
						break
			else:
				break
		
		# print(self.settings)
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')