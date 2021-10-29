#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 14:34:44 2021

@author: cabrown802
"""

import three

three.city('boston')
reqs = three.requests(start='03-10-2021', end='03-17-2021')
print(reqs)


