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
    ima=plt.imread("gris.png")
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
