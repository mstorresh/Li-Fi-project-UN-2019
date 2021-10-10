import Adafruit_BBIO.PWM as PWM

PWM.stop("P8_13")
PWM.start("P8_13",50,10)
PWM.set_duty_cycle("P8_13", 0)


