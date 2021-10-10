import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
#GPIO.setup("P8_16", GPIO.OUT)
#GPIO.output("P8_16", GPIO.LOW)
#cantidad= int(input("deme el  numero: "))
intensidad= PWM.start("P8_13",99,50)
#intensidad.start(100)     #comienza con una frecuencia de 100
PWM.set_frequency("P8_13", 1000000)
#for i in range(255):
#    PWM.set_duty_cycle("P8_13", 0.39*i)
    #GPIO.output("P8_16", GPIO.HIGH)
#    time.sleep(0.5)
    #GPIO.output("P8_16", GPIO.LOW)
    #time.sleep(1)
    #PWM.set_duty_cycle("P8_13", 75.3)
    #PWM.set_frequency("P8_13", 500)
    #GPIO.output("P8_16", GPIO.HIGH)
    #time.sleep(1)
    #GPIO.output("P8_16", GPIO.LOW)
    #time.sleep(0.5)
    #PWM.set_duty_cycle("P8_13",25)
    #time.sleep(0.5)

PWM.set_duty_cycle("P8_13", 100)
