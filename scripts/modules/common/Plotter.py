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
			'markersize': 1,
			'alpha': 0.5
		}
		
	def create_subplot(self, subplot_index, subplots_number, subplot_height_share):
		if subplot_index == 0:
			self.ax.append(plt.subplot2grid((sum(subplot_height_share) , 1), (self.subplot_offset, 0), rowspan = subplot_height_share[subplot_index]))
		else:
			self.ax.append(plt.subplot2grid((sum(subplot_height_share) , 1), (self.subplot_offset, 0), rowspan = subplot_height_share[subplot_index], sharex = self.ax[0]))
		
		self.subplot_offset += subplot_height_share[subplot_index]
		
	def bind_seria_to_subplot(self, seria, subplot_index, seria_format):
		x_ticks = np.arange(0, len(seria), 1)
		seria = np.array(seria).astype(np.double)
		if seria_format['ignoring_missed_data_line']:
			s_mask = np.isfinite(seria)
			self.ax[subplot_index].plot(x_ticks[s_mask], seria[s_mask],
				'.-',
				color = seria_format['color'],
				linewidth = seria_format['linewidth'],
				markersize = seria_format['markersize'],
				alpha = seria_format['alpha']
			)
		else:
			self.ax[subplot_index].plot(x_ticks, seria,
				'.-',
				color = seria_format['color'],
				linewidth = seria_format['linewidth'],
				markersize = seria_format['markersize'],
				alpha = seria_format['alpha']
			)
		
	def plot_series(self, data, settings, fig_name):
		if self.errors.error_occured:
			return None
		
		fig_folder = settings['plotter']['fig_folder']
		series = settings['plotter']['series']
		subplots_number = settings['plotter']['subplots_number']
		subplot_height_share = settings['plotter']['subplot_height_share']
		seria_to_subbplot_binding = settings['plotter']['seria_to_subbplot_binding']
		
		
		# fig = plt.figure(figsize = (16, 9))
		for subplot_index in range(subplots_number):
			self.create_subplot(subplot_index, subplots_number, subplot_height_share)
		
		for seria_index in range(len(series)):
			seria = data[series[seria_index]]
			subplot_index = seria_to_subbplot_binding[seria_index] - 1
			seria_format = {
				'ignoring_missed_data_line': settings['plotter']['ignoring_missed_data_line'][seria_index],
				'linewidth': settings['plotter']['series_linewidth'][seria_index],
				'markersize': settings['plotter']['series_markersize'][seria_index],
				'color': settings['plotter']['series_color'][seria_index],
				'alpha': settings['plotter']['series_alpha'][seria_index]
			}
			self.bind_seria_to_subplot(seria, subplot_index, seria_format)
			
		plt.tight_layout()
		plt.savefig(fig_folder + 'fig' + fig_name + '.png', dpi = 100)
		plt.close()
		
		