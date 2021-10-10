#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:23:06 2019

@author: mstorresh
"""

import numpy as np
import scipy.ndimage as nd
import matplotlib.pyplot as plt
from scipy.misc import imread
from numpy.linalg import inv,lstsq
import scipy.misc as sp 
I=plt.imread("trunks.png")
print(len(I))
print(len(I[0,:]))
I1=(I*255)

imC2= 0.299*I[:,:,0] + 0.587*I[:,:,1] + 0.114*I[:,:,2]
    #Binarización de la blanco y negro
#CB=np.where(imC2<0.5,0,255)

sp.imsave("trunksgris.png",imC2)

