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
		
		
	def plot_series(self, data, settings):
		if self.errors.error_occured:
			return None
		
		series = settings['plotter']['series']
		subplot_height_share = settings['plotter']['subplot_height_share'] 
		subplots_number = settings['plotter']['subplots_number']
		
		print(subplot_height_share)
		
		