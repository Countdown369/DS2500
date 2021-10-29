#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 15:01:58 2021

@author: cabrown802
"""

from random import randrange
import numpy as np
import matplotlib.pyplot as plt

DIMENSTION = 500

image = np.zeros((DIMENSTION, DIMENSTION, 3), dtype = 'int8')


for i in range(DIMENSTION):
    for j in range(DIMENSTION):
        red = i * j % 256
        green = (i*i - j*j) % 256
        blue = (i*i + j*j) % 256
        image[i][j] = [red, randrange(255), blue]

print(image)
plt.figure(figsize = (100,100))
plt.imshow(image, interpolation = "none")