# -*- coding: utf-8 -*

from modules.common.Errors import *
from modules.common.IniParser import *
from modules.common.Tools import *

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
		self.settings['common'] = {}
		self.settings['common']['time_frames'] = tools.int_arr(tools.explode(',', self.ini_parser.get_param('common', 'time_frames')))
		self.settings['contracts'] = {}
		tickers = tools.explode(',', self.ini_parser.get_param('contracts', 'tickers'))
		
		for ticker_idx in  range(len(tickers)):	
			self.settings['contracts'][ticker_idx] = {}
			self.settings['contracts'][ticker_idx]['ticker'] = tickers[ticker_idx]
			self.settings['contracts'][ticker_idx]['list'] = {}
			list = tools.explode(',', self.ini_parser.get_param('contracts', tickers[ticker_idx]))
			for contract_idx in range(len(list)): 
				self.settings['contracts'][ticker_idx]['list'][contract_idx] = self.ini_parser.get_param(list[contract_idx])
			
	def main(self, args):
		self.set_params(args)
		
		contracts = self.settings['contracts']
		for cbt_idx in contracts:
			contracts_by_ticker = contracts[cbt_idx]
			ticker = contracts_by_ticker['ticker']
			list = contracts_by_ticker['list']
			print(ticker);
			for contract_idx in list:
				contract = list[contract_idx]
				ContractSymbol = contract['ContractSymbol']
				ContractTradingSymbol = contract['ContractTradingSymbol']
				FirstTradingDay = contract['FirstTradingDay']
				LastTradingDay = contract['LastTradingDay']
				
				print(ContractTradingSymbol)
			
		
		# print(self.settings)
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')