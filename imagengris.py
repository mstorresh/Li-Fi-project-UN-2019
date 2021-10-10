import numpy as np
import matplotlib.pyplot as plt
import Adafruit_BBIO.PWM as PWM
import time

intensidad=PWM.start("P8_13",99,50)
PWM.set_frequency("P8_13", 1000000)
ima=255*plt.imread("n2.png")
IM=np.ravel(ima)
a=len(IM)

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
time.sleep(1.531)

for i in range(a):
	s=IM[i]*0.39
	PWM.set_duty_cycle("P8_13", s)
	time.sleep(0.002)

PWM.set_duty_cycle("P8_13", 0)        
