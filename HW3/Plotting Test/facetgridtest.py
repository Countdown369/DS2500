#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:44:41 2021

@author: cabrown802
"""

import seaborn as sns

attend = sns.load_dataset("attention").query("subject <= 14")
print(attend)
g = sns.FacetGrid(attend, col="subject", col_wrap=4, height=2, ylim=(0, 10))
g.map(sns.pointplot, "solutions", "score", order=[1, 2, 3], color=".3", ci=None)