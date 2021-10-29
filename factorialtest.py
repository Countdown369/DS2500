#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 19:49:43 2021

@author: cabrown802
"""

def factorial(n):
    product = 1
    for i in range(1, n+1):
        product *= i
    return product

for i in range(10000):
    if i % 1000 == 0:
        print(str(i) + " => " + str(factorial(i)))