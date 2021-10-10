# -*- coding: utf-8 -*-
import Adafruit_BBIO.ADC as ADC
import numpy as np
from time import sleep

ADC.setup()
V = []
t = []
t0 = 0.0
analogPin = "P9_40"
while(1):
#for i in range (0,1000):
	potVal = ADC.read(analogPin) * 1.8
#	t0 += 0.01
#	V.append(potVal)
#	t.append(t0)
	print(potVal)
	sleep(0.01)

#M = np.zeros([len(V),2])
#for i in range (0,len(V)):
#	M[i,0] = t[i]
#	M[i,1] = V[i]

#np.savetxt("data.txt",M,fmt="%10.3E")




