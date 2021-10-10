# cython: language_level=2
# coding: utf-8

# -------------------------------------------------------------------------------
# previous to run this script, the following command must be run:
#   config-pin -f config-pin.config
# to load configuration pin file (in configuration pin file directory)
# -------------------------------------------------------------------------------

import struct
import numpy as np
import matplotlib.pyplot as plt
import time
def toBinary(string):
	l=[]
	for i in range(len(string)):
		l.append(''.join([format(ord(char),'#010b')[2:] for char in string[i]]))
	return l
class Example(object):
    """
    """
    def __init__(self, _=None):

        pass

    def read_adc_from_pru(self):
        return self.talk_with_pru('a')
        
    def binarizar (self, decimal):
		binario=''
		while decimal//2 !=0:
			binario = str(decimal % 2) + binario
			decimal = decimal//2
		if len(binario) ==6:
			return str(0) + str(decimal) + binario
		if len(binario) ==5:
			return str(0)+ str(0) + str(decimal) + binario
		if len(binario) ==4:
			return str(0) +str(0) + str(0) + str(decimal) + binario
		if len(binario) ==3:
			return str(0) + str(0) + str(0) +str(0) + str(decimal) + binario
		if len(binario) ==2:
			return str(0) + str(0) + str(0) +str(0) + str(0) + str(decimal) + binario
		if len(binario) ==1:
			return str(0) + str(0) + str(0) + str(0) + str(0) + str(0) +str(decimal) + binario
		else:
			return str(decimal) + binario

    def pwm_pru(self, duty,frequency):
        """
        Gets/sets the pwm value
        """
        # PWM in C (PRU)

        self.talk_with_pru("p",frequency,duty)

    def talk_with_pru(self, command, d0=0, d1=0, d2=0, d3=0, d4=0):
        """
    Enviar un comando al PRU
    :param command: Cadena de caracteres de maximo 3 letras
    :param d0: Parametro 0 del comando command (entero 32 bits)
    :param d1: Parametro 1 del comando command (entero 32 bits)
    :param d2: Parametro 2 del comando command (entero 32 bits)
    :return: Tupla (command,d0,d1,d2,d3,d4) retornada por el PRU
    """
        command = ('*' + command)[:4]
        with open('/dev/rpmsg_pru30', 'r+') as virtual_device:
            request = struct.pack("4siiiii", command, d0, d1, d2, d3, d4)
            virtual_device.write(request)
            response = struct.unpack("4siiiii", virtual_device.read(24))
        return response


if __name__ == '__main__':
	example = Example()
	clase = str(raw_input("Quiere mandar imagen en: gris, color o texto: "))
	if clase == "gris":
		imagen = str(raw_input("diga la imagen: gris.png , n4.png, 100gris.png, dcgris.png, okgris.png, pokegris.png, trunksgris.png:  "))
		ima = plt.imread(imagen)
		IM=np.ravel(ima)
		IM=(IM*90)+10
		a=len(IM)
		l=[]
		t1=len(ima)
		t2=len(ima[0,:])
		b1=example.binarizar(t1)
		b2 = example.binarizar(t2)
		b3="".join([b1,b2])
		example.pwm_pru(0,100)
		time.sleep(1)
		example.pwm_pru(100,100)
		example.pwm_pru(0,100)
		example.pwm_pru(100,100)
		example.pwm_pru(100,100)
		for i in range(len(b3)):
			print(b3[i])
			if b3[i]=="0":
				example.pwm_pru(0,100)
			if b3[i]=="1":
				example.pwm_pru(100,100)
		example.pwm_pru(0,100)
		time.sleep(2)
		example.pwm_pru(100,100)
		example.pwm_pru(10,100)
		example.pwm_pru(10,100)
		example.pwm_pru(100,100)
		for i in range(len(IM)):
			s = IM[i]
			example.pwm_pru(s,100)
		example.pwm_pru(0,100)
	if clase == "color":
		imagen = str(raw_input("diga la imagen a color: 100.jpeg , index.png, l5.png, lena.png, 100.jpeg, dc.jpg, ok.jpeg, poke.png, trunks.png :   "))
		ima = plt.imread(imagen)
		ima0=ima[:,:,0]
		ima1=ima[:,:,1]
		ima2=ima[:,:,2]
		IM0=np.ravel(ima0)
		a0=len(IM0)
		IM1=np.ravel(ima1)
		a1=len(IM1)
		IM2=np.ravel(ima2)
		a2=len(IM2)
		IM0=IM0*100
		IM1=IM1*100
		IM2=IM2*100
		IM=np.append(IM0,IM1)
		IM=np.append(IM, IM2)
		a=len(IM)
		t1=len(ima0)
		t2=len(ima0[0,:])
		b1=example.binarizar(t1)
		b2 = example.binarizar(t2)
		b3="".join([b1,b2])
		example.pwm_pru(0,100)
		time.sleep(1)
		example.pwm_pru(100,100)
		example.pwm_pru(0,100)
		example.pwm_pru(100,100)
		example.pwm_pru(100,100)
		for i in range(len(b3)):
			print(b3[i])
			if b3[i]=="0":
				example.pwm_pru(0,100)
			if b3[i]=="1":
				example.pwm_pru(100,100)
		example.pwm_pru(0,100)
		time.sleep(2)
		example.pwm_pru(100,100)
		example.pwm_pru(10,100)
		example.pwm_pru(100,100)
		example.pwm_pru(10,100)
		for i in range(a):
			s = IM[i]
			example.pwm_pru(s,100)
		example.pwm_pru(0,100)
	if clase =="texto":
		print("escriba el texto que quiere mandar:")
		s = str(raw_input("--"))
		m = toBinary(s)
		example.pwm_pru(0,100)
		time.sleep(1)
		example.pwm_pru(100,100)
		example.pwm_pru(0,100)
		example.pwm_pru(100,100)
		example.pwm_pru(100,100)
		for i in range(len(s)):
			if s[i]=="0":
				example.pwm_pru(0,100)
			if s[i]=="1":
				example.pwm_pru(100,100)
		example.pwm_pru(0,100)
		time.sleep(2)
		example.pwm_pru(0,100)
		time.sleep(1)
		example.pwm_pru(10,100)
		example.pwm_pru(10,100)
		example.pwm_pru(100,100)
		example.pwm_pru(100,100)
		for i in range(len(m)):
			for j in range(len(m[i])):
				if m[i][j]=="1":
					example.pwm_pru(100,100)
				if m[i][j]=="0":
					example.pwm_pru(0,100)	
		example.pwm_pru(0,100)

		
		
