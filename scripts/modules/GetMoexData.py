# -*- coding: utf-8 -*

import time
import datetime
from datetime import datetime as dt, date #, time
import urllib.request
import urllib.parse

from modules.common.Errors import *
from modules.common.IniParser import *
from modules.common.Tools import *
from modules.common.FileSystem import *

# import urllib.request
# url = 'https://www.moex.com/export/derivatives/currency-rate.aspx?language=ru&currency=USD/RUB&moment_start=2018-12-01&moment_end=2019-04-04'
# page = urllib.request.urlopen(url)
# content = page.read()
# print(content)


class GetMoexData:
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
		self.read_settings(args)
		self.settings['output'] = {}
		self.settings['output']['file_path'] = self.ini_parser.get_param('output', 'file_path')
		
		self.settings['period'] = {}
		self.settings['period']['start_date'] = self.ini_parser.get_param('period', 'start_date')
		
	def shape_moex_url(self, start_date, end_date):
		url = 'https://www.moex.com/export/derivatives/currency-rate.aspx?'
		url = (url + 'language=en' +
			'&currency=USD/RUB' +
			'&moment_start=' + start_date +
			'&moment_end=' + end_date)
		# print(urllib.parse.quote(url))
		return url #urllib.parse.quote(url)

	def extract_rates(self, content):
		saved_content = '<CURRENCY>,<DATE>,<TIME>,<RATE>\n'
		rates = []
		while True:
			rate_moment_pos = content.find('rate moment')
			
			value_pos = content.find('value')
			end_str_pos = content.find('/>')
			
			rate_moment = content[rate_moment_pos+13:value_pos-2]
			value = content[value_pos+7:end_str_pos-2]
			if rate_moment_pos == -1:
				break
			else:
				moment_date = rate_moment.split(' ')[0]
				monent_time = rate_moment.split(' ')[1]
				
				moment_date = dt.strftime(dt.strptime(moment_date, '%Y-%m-%d'), '%Y%m%d')
				monent_time = dt.strftime(dt.strptime(monent_time, '%H:%M:%S'), '%H%M%S')
				rates.append('USDRUB' + ',' + moment_date + ',' + monent_time + ',' + value)

			content = content[end_str_pos + 2:]
		
		rates.sort()
		saved_content += '\n'.join(rates)
			
		return saved_content
	
	def main(self, args):
		self.set_params(args)
		
		fs = FileSystem(self.errors)
		
		
		file_path = self.settings['output']['file_path']
		start_date = self.settings['period']['start_date']

		
		if not self.errors.error_occured:
			start_date = dt.strftime(dt.strptime(start_date, '%d.%m.%Y'), '%Y-%m-%d')
			end_date = dt.strftime((dt.today()), '%Y-%m-%d')
			url = self.shape_moex_url(start_date, end_date)
			content = ''
			try:
				page = urllib.request.urlopen(url)
				content = page.read()
				content = content.decode('utf-8').replace('\r', '')
			except Exception as e:
				self.errors.raise_error('Can\'t open url ' + url + '\n' + str(e))
			

			content = self.extract_rates(content)
			folder_path, file_name = fs.split_file_path(file_path)
			
			fs.create_folder_branch(folder_path)
			try:
				with open(file_path, "w") as text_file:
					print(content, file=text_file)
			except Exception as e:
				self.errors.raise_error('Can\'t write file ' + file_path)
		
		if self.errors.error_occured:
			self.errors.print_errors()
		else:
			print('OK\n')