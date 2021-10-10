
import Adafruit_BBIO.PWM as PWM
import time


def toBinary(string):
	l=[]
	for i in range(len(string)):
		l.append(''.join([format(ord(char),'#010b')[2:] for char in string[i]]))
	return l

intensidad=PWM.start("P8_13",99,50)
PWM.set_frequency("P8_13", 1000000)

s= "a b c d e f g h i j k l m n o p q r s t u v w x y z "   # string que se va a mandar
m = toBinary(s)
#print (m)

PWM.set_duty_cycle("P8_13", 0)
 # comienza con una frecuencia de 100
PWM.set_duty_cycle("P8_13", 100)
time.sleep(0.02)
PWM.set_duty_cycle("P8_13", 0)
time.sleep(0.02) 
PWM.set_duty_cycle("P8_13", 0)
time.sleep(0.02)
PWM.set_duty_cycle("P8_13", 100)
time.sleep(0.02) 
time.sleep(1.5)

for i in range(len(m)):
		for j in range(len(m[i])):
			#print (m[i][j])
			if m[i][j]=="1":
				PWM.set_duty_cycle("P8_13", 100)
				time.sleep(0.05)
			if m[i][j]=="0":
				PWM.set_duty_cycle("P8_13", 0)
				time.sleep(0.05)
				
PWM.set_duty_cycle("P8_13", 0)
#time.sleep(0.5)

