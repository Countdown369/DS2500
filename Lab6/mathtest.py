#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 23:38:52 2021

@author: cabrown802
"""

import sympy
import math
import matplotlib.pyplot as plt

# Circles of r = 1 you can fit around each new circle's circumference
circlesPerCircle = []

# Multiples of pi
pis = []

# Circle list / multiples of pi list
ratios = []

# Make x symbolic to do maths
x = sympy.symbols('x')

# For i, an integer in [1, 20], find how many circles can fit around it.
# Process outlined in my Reddit comment with mostly incorrect computation;
# still, the last paragraph is instructive on what the algorithm below does.
for i in range(2, 26):
    if i % 10 == 0:
        print(str(i))
    intersection_x = sympy.solve(sympy.sqrt(i**2 - x**2) + sympy.sqrt(1 - x**2) - i, x)
    intersection_y = math.sqrt(i**2 - intersection_x[1]**2)
    arclength = sympy.Integral(sympy.sqrt(1 + (((-1 * x)/(i**2 - x**2)) ** 2)), (x, intersection_x[0], intersection_x[1]))
    arclength = arclength.evalf()
    circles = (i * math.pi * 2) / arclength
    circlesPerCircle.append(circles)
    pis.append(math.pi * i)

for i in range(len(pis)):
    ratios.append(circlesPerCircle[i] / pis[i])
    
plt.plot(ratios)
plt.plot ([1 for ratio in ratios])
# plt.ylim([0, 1.05])
plt.draw()

# After 1 circle, we're ~17% off of pi. After 20, we're only 0.03% off of pi.
    




