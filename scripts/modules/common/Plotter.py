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
		
		
	def plot_series(self, data, settings, fig_name):
		if self.errors.error_occured:
			return None
		
		fig_folder = settings['plotter']['fig_folder']
		series = settings['plotter']['series']
		subplot_height_share = settings['plotter']['subplot_height_share'] 
		subplots_number = settings['plotter']['subplots_number']
		
		ax = []
		offset = 0
		for i in range(subplots_number):
			ax.append(plt.subplot2grid((sum(subplot_height_share) , 1),(offset , 0), rowspan = subplot_height_share[i]))
			offset = offset + subplot_height_share[i]
			
		plt.tight_layout()
		plt.savefig(fig_folder + 'fig' + fig_name + '.png', dpi = 100)
		plt.close()
		
		