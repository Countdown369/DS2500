#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 12:55:01 2021

Student: Connor Brown
Date: 10/01/21
Project: Week 4 Lab (Seaborn)
"""

# Neccesary imports
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset about penguins
penguins = sns.load_dataset('penguins')

# Create plot:
# Using the "violin" type to plot penguin flipper lengths of the same species
# as the island a penguin lives on varies.
myPlot = sns.catplot(
    data = penguins, kind = 'violin',
    x = 'species', y = 'flipper_length_mm', hue = 'island')


# Set up labels
myPlot.set_axis_labels("", "Flipper length (mm)")
myPlot.legend.set_title("Island")
plt.title("Flipper Length of Same Species of Penguin Across Various Islands")

"""
Interesting visualization for sure - but it appears the only penguins which
live on more than one island (in my dataset) are the Adelie penguins. See
Plot2.py for the investigation of Adelie penguins.
"""