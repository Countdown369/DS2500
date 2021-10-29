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
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
penguins = sns.load_dataset('penguins')

# Convert dataset to DataFrame, keeping only the Adelie penguins
penguinDF = pd.DataFrame(penguins)
penguinDF = penguinDF[penguinDF.species == 'Adelie']

# Create plot:
# Using some fancy graphic effects here.
# Tried to increase spacing between the bars to be above 0, but
# I couldn't figure this out. :(
myPlot = sns.catplot(
    data = penguinDF, kind = 'bar',
    x = 'species', y = 'flipper_length_mm', hue = 'island',
    ci = "sd", alpha = 0.8, palette = "rocket", aspect = .6)

# Set labels (and ylims, so that comparisons can be better made)
myPlot.set_axis_labels("", "Flipper length (mm)")
myPlot.legend.set_title("Island")
plt.title("Flipper Length of Adelie Penguin Across Various Islands")
plt.ylim((180,200))

"""
Clearly, Adelie penguins of Torgensen Island have a greater flipper length than
those from Dream Island, and Adelie penguins of Dream Island have a greater
flipper length than those from Biscoe Island. I wonder if this is due to
differences in evolution, or just statistical noise.
"""