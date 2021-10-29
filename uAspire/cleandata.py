#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 15:26:18 2021

@author: cabrown802
"""

import pandas as pd

def checkIllegitimateValues(df, column, legitimate):
    print("Checking for " + column + ":")
    for i in df[column]:
        if i not in legitimate:
            print(i)

original = 'original.csv'
salesforce = 'salesforce.csv'

ordf = pd.read_csv(original)
sadf = pd.read_csv(salesforce)

comparison = ordf['EthnicID'].compare(sadf['Ethnic Background'])
print(comparison)
print()

# for town in sadf['MailingCity']:
#     if town not in ["Jamaica Plain", "Boston", "West Roxbury", "Dorchester", \
#                     "Hyde Park", "Roslindale", "Mattapan", "Randolph", \
#                         "Readville", "Taunton"]:
#         print(town)
    
# for grade in sadf['Grade']:
#     if grade not in [9, 10, 11, 12]:
#         print(grade)
        
# for gender in sadf['Gender']:
#     if gender not in ["Non-Binary", "Male", "Female"]:
#         print(gender)
        
checkIllegitimateValues(sadf, 'MailingCity', ["Jamaica Plain", "Boston", "West Roxbury", "Dorchester", \
                    "Hyde Park", "Roslindale", "Mattapan", "Randolph", \
                        "Readville", "Taunton"])
checkIllegitimateValues(sadf, 'Grade', [9, 10, 11, 12])
checkIllegitimateValues(sadf, 'Gender', ["Non-Binary", "Male", "Female"])

import pdb; pdb.set_trace()

"""
Use Google Sheets / the original source
"""