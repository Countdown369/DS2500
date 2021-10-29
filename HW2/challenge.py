#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 15:13:10 2021

Student: Connor Brown
Date: 10/10/21
Project: Homework 02: The Challenger Accident
"""

# Neccesary imports
import pandas as pd
from io import StringIO
from csv import writer 
import math
import numpy as np
import matplotlib.pyplot as plt

# Credit to geeksforgeeks.org and prakhar7 for the haversine distance function:
# https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
# It imagines the Earth as a sphere instead of an oblate spheroid, but nobody
# wants to use Vincenty's formulae, so here goes.
def haversine(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

# Declare our first stats file
stat_file = "stations.csv"

# Using CSV Writer is much more efficient than adding these rows to the
# dataframe directly every time, as appending rows forces the entire structure
# to reload. Thanks to Tom Harvey / ximiki:
# https://stackoverflow.com/questions/41888080/python-efficient-way-to-add-rows-to-dataframe
output = StringIO()
csv_writer = writer(output)

# Index 'counter' will make sire we don't view the extra ~10% of rows at the end of the
# CSV which contain no usable data
counter = 1

# Read the data into the in-memory CSV
with open(stat_file, "r") as textfile:
    for r in textfile:
        datalist = r.split(",")
        if counter < 30000:
            try:
                csv_writer.writerow([int(datalist[0]),
                           float(datalist[2]),
                           float(datalist[3])])
                counter += 1
                
            except ValueError:
                counter += 1
                pass

# Go back to the beginning of the CSV, then make a DF from it
output.seek(0)
coords = pd.read_csv(output, names = ["StationID", "Latitude", "Longitude"])
coords = coords.drop(coords[(coords.Latitude == 0) | (coords.Longitude == 0)].index)

print("ORIGINAL COORDS DF DONE")
coordsJan = coords.copy(deep=True)

# Cape Canaveral coordinates
CC = [28.3922, -80.6077]

# Figure out distances of each station from Cape Canaveral and make this a DF
output2 = StringIO()
csv_writer2 = writer(output2)

for index, row in coords.iterrows():
    csv_writer2.writerow([haversine(row['Latitude'], row['Longitude'], CC[0], CC[1])])

output2.seek(0)
isitclose = pd.read_csv(output2, names = ["Close"])
isitclose = isitclose[~(isitclose['Close'] > 100)]

print("STATIONS < 100 KM AWAY IDENTIFIED")

# Store coords as it currently is for part B. We're about to make coords
# contain only stations which are adequately close to Cape Canaveral (< 100 km)

# I love this next line.
# It combines the two dataframes, removing all stations which are not within
# the "isitclose" dataframe. Thanks, inner join!
coords = coords.join(isitclose, how = 'inner')

print("COORDS AND DISTANCE MERGED")

# Start loading in temperatures. This load will be specific to Part A.
stat_file2 = "temp_1986.csv"
output3 = StringIO()
csv_writer3 = writer(output3)

with open(stat_file2, "r") as textfile:
    for r in textfile:
        datalist = r.split(",")
        try:
            """
            IMPORTANT:
            Only ONE station makes it out of these if statements such that
            it can be used for getting data about Cape Canaveral in January,
            1986. This is Station 722108, stationed out of Southwest Florida
            International Airport in Fort Meyers, FL. It's worth mentioning
            this because it removes the need for me to loop through multiple
            locations, making much of my work easier.
            
            To be clear, this station satisfies these conditions, which no
            other station does:
            1. Within 100 km of Cape Canaveral
            2. Is mentioned by Station ID in both the temperature data and
            coordinate data CSVs
            3. Has data for January 1986
            """
            if int(datalist[0]) in coords['StationID'].tolist():
                if int(datalist[2]) == 1:
                    csv_writer3.writerow([int(datalist[0]),int(datalist[3]),float(datalist[4].rstrip())])
        except ValueError:
            pass

# Put data in dataframe
output3.seek(0)
temps = pd.read_csv(output3, names = ["StationID", "JanDay", "Temp"])
coords = coords.merge(temps)
print("COORDS, DISTANCES, AND TEMPS MERGED")


CCtemps = []
    
# This code is built to work with more than one station. The outer loop loops
# 31 times for all the days in January, and the inner loop loops over all rows
# of coords whose indicies are congruent to the first row index mod 31.
# (For example, the 0th row calculations will also take care of the 31st row,
# the 62nd row, etc. because these rows correspond to the same day for a
# different station.)
for j in range(31):
    for i in range(0, len(coords), 31):
        numerator = []
        denominator = []
        numerator.append(coords.loc[j+i]['Temp']/coords.loc[j+i]['Close'])
        denominator.append(1/coords.loc[j+i]['Close'])
    CCtemps.append(float(sum(numerator)/sum(denominator)))

# If you really want to know the temperature in Cape Canaveral the day of
# the Challenger disaster, it's stored in this variable.
CC28 = CCtemps[27]

# Plot line chart.
plt.plot(range(1,32),CCtemps)
plt.title('Approximate Temperature of Cape Canaveral (January 1986)')
plt.xlabel('Day of January')
plt.ylabel('Temperature (Degrees Fahrenheit)')
plt.xlim([1,31])
plt.text(18.8, 49, "Challenger disaster")
plt.plot(28, 49,'ro') 
plt.show()

print("PART A DONE")

# Load in temperature data again for Part B.

output4 = StringIO()
csv_writer4 = writer(output4)

# Loop-neccesary variables
checkagainst = coordsJan['StationID'].tolist()
counter2 = 0
dupls = []

# The first read-in will get us data for 1/28
with open(stat_file2, "r") as textfile:
    for r in textfile:
        counter2+= 1
        if '28' not in r:
            continue
        if counter2 % 1000000 == 0:
            print("Working on US Temps... (Jan 28) " + str(counter2) + "/2436910")
        datalist = r.split(",")
        try:
            if int(datalist[0]) in checkagainst:
                if '01' in datalist:
                    if datalist[0] not in dupls:
                        dupls.append(datalist[0])
                        csv_writer4.writerow([int(datalist[0]),float(datalist[4].rstrip())])
        except ValueError:
            pass

output4.seek(0)
ustemps128 = pd.read_csv(output4, names = ["StationID", "Temp"])

print("DATA FOR USA 01/28/86 PARSED")
# The second read-in will get us data for 2/1
counter2 = 0

output5 = StringIO()
csv_writer5 = writer(output5)
dupls2 = []

with open(stat_file2, "r") as textfile:
    for r in textfile:
        counter2+= 1
        if '01' not in r or '02' not in r:
            continue
        if counter2 % 5000 == 0:
            print("Working on US Temps... (Feb 1) " + str(counter2) + "/2436910")
        datalist = r.split(",")
        try:
            if int(datalist[0]) in checkagainst:
                if datalist[2] == '02' and datalist[3] == '01':
                    if datalist[0] not in dupls2:
                        dupls2.append(datalist[0])
                        csv_writer5.writerow([int(datalist[0]),float(datalist[4].rstrip())])
        except ValueError:
            pass

output5.seek(0)
ustemps201 = pd.read_csv(output5, names = ["StationID", "Temp"])

print("DATA FOR USA 02/01/86 PARSED")

# Merge coordinate dataframes with more complete temperature dataframe
coordsFeb = coordsJan.copy(deep=True)
coordsFeb = coordsFeb.merge(ustemps201)
coordsJan = coordsJan.merge(ustemps128)

# Create lists of rows and indexes of the 1/28 data and 2/1 data.
# This'll allow us to check it without re-calling iterrows() thousands of times
oneTimeJan = list(coordsJan.iterrows())
oneTimeFeb = list(coordsFeb.iterrows())


print("PART B DATA FILTERED")

# Begin gathering data into numpy arrays for image plotting

# Much of the below code is modelled from the 'numpy_image.py' file shared on
# Canvas. My thanks to the professors of DS2500 for uploading this file.

# Setup vars
XSIZE = 100
YSIZE = 150

COLORS = [[255, 0, 0],
          [255, 25, 25],
          [255, 51, 51],
          [255, 76, 76],
          [255, 102, 102],
          [255, 127, 127],
          [255, 153, 153],
          [255, 178, 178],
          [255, 204, 204],
          [255, 229, 229],
          [255, 255, 255]]

# This first code structure fills the jangrid with data about temperatures
# at every "pixel" of our image using inverse distance weighting.
newcount = 0
jangrid = np.zeros((XSIZE, YSIZE), dtype = int)
for i in range(XSIZE):
    # This code takes ~ 10 minutes to run, so print out progress each 1%.
    print(str(i) + "/100")
    for j in range(YSIZE):
        newcount += 1
        
        # These vars reflect the Earth-coordinates of any jangrid[i, j]
        latitude = 0.25 * i + 25
        longitude = 0.4 * j - 125
        
        # Start of inverse distance weighting algorithm
        numerator = []
        denominator = []
        for index, row in oneTimeJan:
            # Will only apply to stations < 1000 km away from the coordinate
            if haversine(row['Latitude'], row['Longitude'], latitude, longitude) < 1000:
                try:
                    numerator.append(row['Temp']/haversine(row['Latitude'], row['Longitude'], latitude, longitude))
                # If we have no data, essentially set the point to a garbage value
                except ZeroDivisionError:
                    jangrid[i, j] = 11111
                    continue
                try:
                    denominator.append(1/haversine(row['Latitude'], row['Longitude'], latitude, longitude))
                except ZeroDivisionError:
                    jangrid[i, j] = 11111
                    continue
        # Complete the inverse distance weight algorithm, or if it fails,
        # insert a garbage value of 11111
        try:
            jangrid[i, j] = float(sum(numerator)/sum(denominator))
        except:
            jangrid[i, j] = 11111

# Now set up the image array...
janimage = np.zeros((XSIZE, YSIZE, 3), dtype = int)  

for i in range(XSIZE):
    for j in range(YSIZE):
        # Big if-statement checking what the temperature is and assigning a
        # color based on that temp. Lighter red means colder, black means that
        # we have no data.
        if jangrid[i, j] < 0:
            janimage[XSIZE - i - 1, j] = COLORS[10]
        elif jangrid[i, j] < 10:
            janimage[XSIZE - i - 1][j] = COLORS[9]
        elif jangrid[i, j] < 20:
            janimage[XSIZE - i - 1][j] = COLORS[8]
        elif jangrid[i, j] < 30:
            janimage[XSIZE - i - 1][j] = COLORS[7]
        elif jangrid[i, j] < 40:
            janimage[XSIZE - i - 1][j] = COLORS[6]
        elif jangrid[i, j] < 50:
            janimage[XSIZE - i - 1][j] = COLORS[5]
        elif jangrid[i, j] < 60:
            janimage[XSIZE - i - 1][j] = COLORS[4]
        elif jangrid[i, j] < 70:
            janimage[XSIZE - i - 1][j] = COLORS[3]
        elif jangrid[i, j] < 80:
            janimage[XSIZE - i - 1][j] = COLORS[2]
        elif jangrid[i, j] < 90:
            janimage[XSIZE - i - 1][j] = COLORS[1]
        elif jangrid[i, j] < 100:
            janimage[XSIZE - i - 1][j] = COLORS[0]
        else:
            janimage[XSIZE - i - 1][j] = [0, 0, 0]

# Show the plot
plt.figure(figsize = (10,10))
plt.imshow(janimage, interpolation = "none")
plt.show()

# Do the same thing, but with data from 2/1
newcount = 0
febgrid = np.zeros((XSIZE, YSIZE), dtype = int)
for i in range(XSIZE):
    print(str(i) + "/100")
    for j in range(YSIZE):
        newcount += 1
        latitude = 0.25 * i + 25
        longitude = 0.4 * j - 125
        numerator = []
        denominator = []
        for index, row in oneTimeFeb:
            if haversine(row['Latitude'], row['Longitude'], latitude, longitude) < 1000:
                try:
                    numerator.append(row['Temp']/haversine(row['Latitude'], row['Longitude'], latitude, longitude))
                except:
                    febgrid[i, j] = 11111
                try:
                    denominator.append(1/haversine(row['Latitude'], row['Longitude'], latitude, longitude))
                except:
                    febgrid[i, j] = 11111
        try:
            febgrid[i, j] = float(sum(numerator)/sum(denominator))
        except:
            febgrid[i, j] = 11111

febimage = np.zeros((XSIZE, YSIZE, 3), dtype = int)  

for i in range(XSIZE):
    for j in range(YSIZE):
        if febgrid[i, j] < 0:
            febimage[XSIZE - i - 1, j] = COLORS[10]
        elif febgrid[i, j] < 10:
            febimage[XSIZE - i - 1][j] = COLORS[9]
        elif febgrid[i, j] < 20:
            febimage[XSIZE - i - 1][j] = COLORS[8]
        elif febgrid[i, j] < 30:
            febimage[XSIZE - i - 1][j] = COLORS[7]
        elif febgrid[i, j] < 40:
            febimage[XSIZE - i - 1][j] = COLORS[6]
        elif febgrid[i, j] < 50:
            febimage[XSIZE - i - 1][j] = COLORS[5]
        elif febgrid[i, j] < 60:
            febimage[XSIZE - i - 1][j] = COLORS[4]
        elif febgrid[i, j] < 70:
            febimage[XSIZE - i - 1][j] = COLORS[3]
        elif febgrid[i, j] < 80:
            febimage[XSIZE - i - 1][j] = COLORS[2]
        elif febgrid[i, j] < 90:
            febimage[XSIZE - i - 1][j] = COLORS[1]
        elif febgrid[i, j] < 100:
            febimage[XSIZE - i - 1][j] = COLORS[0]
        else:
            febimage[XSIZE - i - 1][j] = [0, 0, 0]

plt.figure(figsize = (10,10))
plt.imshow(febimage, interpolation = "none")
plt.show()