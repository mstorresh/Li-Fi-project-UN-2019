import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_16", GPIO.OUT)

#for i in range(100):
#	if i%2==0:
#		GPIO.output("P8_14", GPIO.HIGH)
#		time.sleep(0.5)
#	else:
#		GPIO.output("P8_14",GPIO.LOW)
#		time.sleep(0.5)

GPIO.output("P8_16",GPIO.LOW)




