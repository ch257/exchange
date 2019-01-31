# -*- coding: utf-8 -*

from modules.indicators.Buffer import *
from modules.indicators.SMA import *

b = Buffer(3)

for i in range(10):
	b.slide(i)
	if b.is_ready:
		print(b.buff)
		
		
sma = SMA(3)
for i in range(1,10,1):
	val = sma.calc(i)
	print(i, val)