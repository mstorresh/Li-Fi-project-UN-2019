import numpy as np
import matplotlib.pyplot as plt
import Adafruit_BBIO.GPIO as GPIO
import time

ima=plt.imread("n2.png")
IM=np.ravel(ima)
a=len(IM)


GPIO.setup("P8_16", GPIO.OUT)
 # comienza con una frecuencia de 100
GPIO.output("P8_16", GPIO.HIGH)
time.sleep(0.01)
GPIO.output("P8_16", GPIO.LOW)
time.sleep(0.01)
GPIO.output("P8_16", GPIO.HIGH)
time.sleep(0.01)
GPIO.output("P8_16", GPIO.LOW)
time.sleep(0.01)
time.sleep(1.52)

for i in range(a):
    if IM[i] ==1 :
         GPIO.output("P8_16", GPIO.HIGH)
         time.sleep(0.002)
    if IM[i] == 0:
         GPIO.output("P8_16", GPIO.LOW)
         time.sleep(0.002)

GPIO.output("P8_16", GPIO.LOW)
