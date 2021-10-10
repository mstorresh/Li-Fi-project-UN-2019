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
    s = "123"
    m = toBinary(s)
    example.pwm_pru(0,100)
    time.sleep(1)
    example.pwm_pru(100,100)
    example.pwm_pru(0,100)
    example.pwm_pru(100,100)
    example.pwm_pru(100,100)
    for i in range(len(b3)):
		print(b3[i])
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
			#print (m[i][j])
			if m[i][j]=="1":
				example.pwm_pru(100,100)
			if m[i][j]=="0":
				example.pwm_pru(0,100)	
    example.pwm_pru(0,100)
