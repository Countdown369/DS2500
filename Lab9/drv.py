#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:50:40 2021

@author: rachlin
"""

import random as rnd
import matplotlib.pyplot as plt 
from collections import Counter
import seaborn as sns 


    
class DRV:
    

    def __init__(self, dist = {}, trials=10000):
        """ Constructor """
        self.dist = dist
        DRV.trials = trials

    def add_value(self, x, p):
        """ Add a value to the DRV with probability p """
        self.dist[x] = p
        
    def P(self, x):
        """ Get the probability associated with the value x """
        return self.dist.get(x, 0)

    def random(self):
        """ return a random value in accordance with the DRV probability 
        distribution """
        return rnd.choices(list(self.dist.keys()), list(self.dist.values()))[0]

    def E(self):
        """ Expected value """
        ev = 0.0
        for x,p in self.dist.items():
            ev += x * p
        return ev

    @staticmethod
    def toDRV(vals):
        """ Convert a series of values to the corresponding discrete random variable """
        c = Counter(vals)
        total = sum(c.values())
        dist = {k:v/total for k, v in c.items()}
        return DRV(dist)

    def __add__(self, other):
        """ Add two discrete random variables """
        return DRV.toDRV([self.random() + other.random() for i in range(DRV.trials)])

    def __radd__(self, a):
        """ Add a scalar, a, by the DRV """
        return DRV.toDRV([a + self.random() for i in range(DRV.trials)])

    def __sub__(self, other):
        """ Subtract two discrete random variables  """
        return DRV.toDRV([self.random() - other.random() for i in range(DRV.trials)])

    def __rsub__(self, a):
        """ Subtract discrete random variable from scalar  """
        return DRV.toDRV([a - self.random() for i in range(DRV.trials)])

    def __mul__(self, other):
        """ Multiply two discrete random variables  """
        return DRV.toDRV([self.random() * other.random() for i in range(DRV.trials)])

    def __rmul__(self, a):
        """ Multiply a scalar, a, by the DRV """
        return DRV.toDRV([a * self.random() for i in range(DRV.trials)])

    def __truediv__(self, other):
        """ Divide two discrete random variables (TODO: Support scalar) """
        return DRV.toDRV([self.random() / other.random() for i in range(DRV.trials)])

    def __pow__(self, other):
        """ Multiply two discrete random variables (TODO: Support scalar) """
        return DRV.toDRV([self.random() ** other.random() for i in range(DRV.trials)])

    def __repr__(self):
        """ String representation of the DRV """
        
        xp = sorted(list(self.dist.items()))
        
        rslt = ''
        for x,p in xp:
            # I changed this...why were we rounding???
            rslt += str(x) + ' : '+ str(p) + '\n'
        return rslt 
    
    
    

        
    def plot(self, title='', xscale='', yscale='', trials=10000, bins=20, show_cumulative = True):
        """ Display the DRV distribution """

        sample = [self.random() for i in range(trials)]

        sns.displot(sample, kind='hist', stat='probability', bins=bins)
        plt.title(title)
        plt.xlabel('value')

        plt.grid()

        if xscale == 'log':
            plt.xscale(xscale)
            
        if yscale == 'log':
            plt.yscale(yscale)
          
        if show_cumulative: 
            plt.yticks([0.0, 0.25, 0.50, 0.75, 1.00])
            xp = sorted(list(self.dist.items()))
            xval = [t[0] for t in xp]
            pval = [t[1] for t in xp]
            totalp = 0.0
            pcumul = []
            for p in pval:
                totalp += p
                pcumul.append(totalp)
            sns.lineplot(x=xval, y=pcumul)

        plt.show()
        
        
    
            
            
        
