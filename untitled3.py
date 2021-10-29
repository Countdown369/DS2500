#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 22:39:35 2021

@author: cabrown802
"""
num = 209

for i in range(206, 0, -3):
    num *= i
    print(str(num) + "\n209!!! after " + str(int((206 - i)/3)) + " steps.")
    print("We just multiplied by " + str(int(i)))
    print()