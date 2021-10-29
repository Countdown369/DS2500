#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:41:54 2021

Student: Connor Brown
Date: 09/16/21
Project: Week 2 Lab (Sunspots)
"""

# Make neccesary imports
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Declare neccesary variables
stat_file = "SN_m_tot_V2.0.csv"

# One list to keep track of dates, and one to keep track of sunspot values
years = []
sunspots = []

# Read data from csv file into respective lists
with open(stat_file, "r") as textfile:
    for r in textfile:
        datalist = r.split(";")
        years.append(float(datalist[2]))
        sunspots.append(float(datalist[3].strip()))
 
# Use numpy functions to find peaks of sunspot activity.
# First, turn list into an array
sunarr = np.array(sunspots)
# Then, use find_peaks() with kwargs to find local maxima
toptimes = find_peaks(sunarr, height = 90, distance = 70)

# Set up variable for computing difference in time between peaks
spot_intervals = []

# Take the differences between elements in our peak dates array;
# this will tell us how long there are in between peaks.
for j in range (1, len(toptimes[0])):
    spot_intervals.append(toptimes[0][j] - toptimes[0][j-1])

# Divide the differences by 12 to convert months to years
for k in range(len(spot_intervals)):
    spot_intervals[k] = spot_intervals[k]/12

def main():
    
    # Add plot labels
    plt.xlabel("Year")
    plt.ylabel("Average Daily Sunspots")
    plt.title("Average Daily Sunspots by Month from 1749 - 2021")
    
    # Plot data
    plt.plot(years, sunspots)
    
    # Return sunspot cycle length in years
    return(np.average(spot_intervals))

main()

"""
The result of the above line is my estimate for the length of a sunspot cycle
in years. This result is approximately 10.2 years.
"""