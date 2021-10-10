
import numpy as np
import matplotlib.pyplot as plt
import Adafruit_BBIO.PWM as PWM
import time

intensidad=PWM.start("P8_13",99,50)
PWM.set_frequency("P8_13", 1000000)
ima=plt.imread("l5.png")
ima0=255*ima[:,:,0]
ima1=255*ima[:,:,1]
ima2=255*ima[:,:,2]
IM0=np.ravel(ima0)
a0=len(IM0)
IM1=np.ravel(ima1)
a1=len(IM1)
IM2=np.ravel(ima2)
a2=len(IM2)
IM = np.append(IM0, IM1)
IM = np.append(IM, IM2)
a = len(IM) 

PWM.set_duty_cycle("P8_13", 0)
 # comienza con una frecuencia de 100
PWM.set_duty_cycle("P8_13", 100)
time.sleep(0.02)
PWM.set_duty_cycle("P8_13", 0)
time.sleep(0.02) 
PWM.set_duty_cycle("P8_13", 100)
time.sleep(0.02)
PWM.set_duty_cycle("P8_13", 0)
time.sleep(0.02) 
time.sleep(1.53032)

for i in range(a0):
	s=IM0[i]*0.39
	PWM.set_duty_cycle("P8_13", s)
	time.sleep(0.002)
time.sleep(1.501)

for i in range(a1):
	s=IM1[i]*0.39
	PWM.set_duty_cycle("P8_13", s)
	time.sleep(0.002)
time.sleep(1.501)

for i in range(a2):
	s = IM2[i]*0.39
	PWM.set_duty_cycle("P8_13", s)
	time.sleep(0.002)

PWM.set_duty_cycle("P8_13",0)
