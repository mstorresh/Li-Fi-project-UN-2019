
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import Adafruit_BBIO.ADC as ADC
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

ADC.setup()
analogPin = "P9_33"
l1=[]
l2=[]

for t in range(100):
    potVal=ADC.read(analogPin)*1.8
    if potVal > 0.4:
        l1.append(1)
    else:
        l1.append(0)
        sleep(0.02)
    print(potVal)
    if(l1==[1,0,1,0]):
        for i in range(64*64):
            potVal=ADC.read(analogPin)*1.8
            if potVal > 0.4:
                l2.append(1)
            else:
                l2.append(0)
            sleep(0.02)
        break
    elif(len(l1)==4):
        l1.pop(0)
    print(l1)
#imagen=np.reshape(l2,(64,64))
np.savetxt("data.txt",l2,fmt="%1.0E")
#ima=plt.imshow(imagen,cmap=plt.cm.gray)
#ima.savefig("prueba.png")
