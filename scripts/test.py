# -*- coding: utf-8 -*

from modules.indicators.Buffer import *

b = Buffer(3)

for i in range(10):
	b.slide(i)
	if b.is_ready:
		print(b.buff)