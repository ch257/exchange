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
		self.default_chart_params = {
			'line': '-',
			'marker': '.',
			'color': 'r', 
			'linewidth': 1,
			'markersize': 5,
			'alpha': 0.5
		}
		
	def create_subplot(self, subplot_index, subplots_number, subplot_height_share):
		if subplot_index == 0:
			self.ax.append(plt.subplot2grid((sum(subplot_height_share) , 1), (self.subplot_offset, 0), rowspan = subplot_height_share[subplot_index]))
		else:
			self.ax.append(plt.subplot2grid((sum(subplot_height_share) , 1), (self.subplot_offset, 0), rowspan = subplot_height_share[subplot_index], sharex = self.ax[0]))
		
		self.subplot_offset += subplot_height_share[subplot_index]
		
	def bind_seria_to_subplot(self, seria, subplot_index):
		x_ticks = np.arange(0, len(seria), 1)
		seria = np.array(seria).astype(np.double)
		s_mask = np.isfinite(seria)
		# self.ax[subplot_index].plot(x_ticks[s_mask], seria[s_mask],
			# self.default_chart_params['type'],
			# color = self.default_chart_params['color'],
			# linewidth = self.default_chart_params['linewidth'],
			# alpha = self.default_chart_params['alpha']
		# )
		self.ax[subplot_index].plot(x_ticks[s_mask], seria[s_mask],
			self.default_chart_params['color'] +
			self.default_chart_params['marker'] +
			self.default_chart_params['line'],
			# 'ro-',
			linewidth = self.default_chart_params['linewidth'],
			markersize = self.default_chart_params['markersize'],
			alpha = self.default_chart_params['alpha']
		)
		
	def plot_series(self, data, settings, fig_name):
		if self.errors.error_occured:
			return None
		
		fig_folder = settings['plotter']['fig_folder']
		series = settings['plotter']['series']
		subplots_number = settings['plotter']['subplots_number']
		subplot_height_share = settings['plotter']['subplot_height_share']
		seria_to_subbplot_binding = settings['plotter']['seria_to_subbplot_binding']
		
		for subplot_index in range(subplots_number):
			self.create_subplot(subplot_index, subplots_number, subplot_height_share)
		
		for seria_index in range(len(series)):
			seria = data[series[seria_index]]
			subplot_index = seria_to_subbplot_binding[seria_index] - 1

			self.bind_seria_to_subplot(seria, subplot_index)
			
		plt.tight_layout()
		plt.savefig(fig_folder + 'fig' + fig_name + '.png', dpi = 100)
		plt.close()
		
		