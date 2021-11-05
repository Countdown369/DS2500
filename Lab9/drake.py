#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:53:18 2021

@author: cabrown802
"""

from drv import DRV
import numpy as np

# Function helpful for constructing DRV objects of uniform distributions.
def uniformDRV(istart, estop, step, p):
    myDict = {}
    for i in np.arange(istart, estop, step):
        myDict[i] = p
    return myDict

def main():
    # Uniform distribution
    rs = DRV(uniformDRV(1.5, 3.5, 0.5, 0.25))
    
    # Bell-shaped distribution
    fp = DRV({0.9: 0.1, 1.0: 0.8, 1.1: 0.1})
    
    # More uniform distributions
    ne = DRV(uniformDRV(1, 6, 1, 0.2))
    f1 = DRV(uniformDRV(0, 0.2, 0.01, 0.05))
    fi = DRV(uniformDRV(0.1, 0.5, 0.1, 0.25))
    fc = DRV(uniformDRV(0.1, 0.5, 0.1, 0.25))
    
    # More likely to be communicating the older the civilization is,
    # but gets cut off at 2100 years of interstellar communication.
    #TheGreatFilter
    
    # By the way, all distributions are constructed such that the sum total
    # probability within the range where p != 0 is 1, just like a real pdf!
    lDict = {}
    for i in np.arange(100, 2200, 100):
        lDict[i] = i/23100
    L = DRV(lDict)
    
    (rs * fp * ne * f1 * fi * fc * L).plot(title = 'Probability Distrubution for Number of Communicating Civilizations in the Milky Way')

    print((rs * fp * ne * f1 * fi * fc * L).E())
    
    """
    The above print statement reports that there are ~55-60 actively
    communicating extraterrestrial civilizations in the Milky Way galaxy.
    So, Fermi, why haven't they hit our line yet?
    """
    
main()