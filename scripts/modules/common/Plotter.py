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
			plt.setp(self.ax[subplot_index].get_xticklabels(), visible = False)
			self.ax[subplot_index].grid(which = 'minor', alpha = 0.4)
			self.ax[subplot_index].grid(which = 'major', alpha = 1)
			
		else:
			self.ax.append(plt.subplot2grid((sum(subplot_height_share) , 1), (self.subplot_offset, 0), rowspan = subplot_height_share[subplot_index], sharex = self.ax[0]))
			plt.setp(self.ax[subplot_index].get_xticklabels(), visible = False)
			self.ax[subplot_index].grid(which = 'minor', alpha = 0.4)
			self.ax[subplot_index].grid(which = 'major', alpha = 1)
		
		self.subplot_offset += subplot_height_share[subplot_index]
		
	def bind_seria_to_subplot(self, seria, subplot_index, seria_format):
		x_ticks = np.arange(0, len(seria), 1)
		seria = np.array(seria).astype(np.double)
		if seria_format['ignoring_missed_data_line']:
			s_mask = np.isfinite(seria)
			self.ax[subplot_index].plot(x_ticks[s_mask], seria[s_mask],
				seria_format['marker'] + '-',
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
		
	def set_seria_format(self, seria_index, settings):
		return {
			'ignoring_missed_data_line': settings['plotter']['ignoring_missed_data_line'][seria_index],
			'linewidth': settings['plotter']['series_linewidth'][seria_index],
			'marker': settings['plotter']['series_marker'][seria_index],
			'markersize': settings['plotter']['series_markersize'][seria_index],
			'color': settings['plotter']['series_color'][seria_index],
			'alpha': settings['plotter']['series_alpha'][seria_index]
		}
		
	def set_x_labels(self, subplots_number):
		minor_x_ticks = [0,4,8,12,16,20,24,28]
		major_x_ticks = [12,24]
		self.ax[0].set_xticks(minor_x_ticks, minor = True)
		self.ax[0].set_xticks(major_x_ticks)
		plt.setp(self.ax[subplots_number - 1].get_xticklabels(), visible = True)
		
	def plot_series(self, data, settings, fig_name):
		if self.errors.error_occured:
			return Noneself
		
		fig_folder = settings['plotter']['fig_folder']
		series = settings['plotter']['series']
		subplots_number = settings['plotter']['subplots_number']
		subplot_height_share = settings['plotter']['subplot_height_share']
		seria_to_subbplot_binding = settings['plotter']['seria_to_subbplot_binding']
		# minor_x_labels = settings['plotter']['minor_x_labels']
		# major_x_labels = settings['plotter']['major_x_labels']
		
		# fig = plt.figure(figsize = (16, 9))
		for subplot_index in range(subplots_number):
			self.create_subplot(subplot_index, subplots_number, subplot_height_share)
		
		for seria_index in range(len(series)):
			seria = data[series[seria_index]]
			subplot_index = seria_to_subbplot_binding[seria_index] - 1
			seria_format = self.set_seria_format(seria_index, settings)
			self.bind_seria_to_subplot(seria, subplot_index, seria_format)
			
		self.set_x_labels(subplots_number)
			
		plt.tight_layout()
		plt.savefig(fig_folder + 'fig' + fig_name + '.png', dpi = 100)
		plt.close()
		
		