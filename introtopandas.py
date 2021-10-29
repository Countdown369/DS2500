#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 13:45:15 2021

@author: cabrown802
"""

import numpy as np
import pandas as pd

grades = {'Wally': [1, 2, 3], 'Eva': [4,5,6], 'Bob': [7,8,9], 'Al': [10,11,12]}

grades2 = pd.DataFrame(grades, index = ['T1','T2', 'T3'])

print(grades2.loc['T1'])