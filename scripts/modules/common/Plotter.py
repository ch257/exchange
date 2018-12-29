# -*- coding: utf-8 -*

import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import matplotlib.ticker as mticker
# from matplotlib.finance import candlestick_ohlc
# from matplotlib import style

# import numpy as np
# import datetime as dt

class Plotter:
	def __init__(self, errors):
		self.errors = errors
		self.settings = {}
		self.ax = []
		self.subplot_offset = 0
		
	def create_subplot(self, subplot_index, subplots_number, subplot_height_share):
		if subplot_index == 0:
			self.ax.append(plt.subplot2grid((sum(subplot_height_share) , 1), (self.subplot_offset, 0), rowspan = subplot_height_share[subplot_index]))
		else:
			self.ax.append(plt.subplot2grid((sum(subplot_height_share) , 1), (self.subplot_offset, 0), rowspan = subplot_height_share[subplot_index], sharex = self.ax[0]))
		
		self.subplot_offset += subplot_height_share[subplot_index]
		
	def plot_series(self, data, settings, fig_name):
		if self.errors.error_occured:
			return None
		
		fig_folder = settings['plotter']['fig_folder']
		series = settings['plotter']['series']
		subplots_number = settings['plotter']['subplots_number']
		subplot_height_share = settings['plotter']['subplot_height_share'] 
		
		for subplot_index in range(subplots_number):
			self.create_subplot(subplot_index, subplots_number, subplot_height_share)
			
		plt.tight_layout()
		plt.savefig(fig_folder + 'fig' + fig_name + '.png', dpi = 100)
		plt.close()
		
		