#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 12:19:11 2021

Student: Connor Brown
Date: 10/15/21
Project: Week 6 Lab (Cosine Similarity)
"""

import wordcloud as wc
import matplotlib.pyplot as plt
from collections import Counter

# This function takes in a text file and returns a list of each word in the
# file.
def listOfWords(txt):
    listOfWords = []
    with open(txt, "r") as textfile:
        for r in textfile:
            datalist0 = r.split(" ")
            datalist = []
            for i in range(len(datalist0)):
                datalist0[i] = datalist0[i].strip()
                
            for i in range(len(datalist0)):
                try:
                    datalist0[i] = datalist0[i].lower()
                except:
                    datalist[i] = ""
            for word in datalist0:
                if len(word) > 0:
                    datalist.append(word.replace("[", "").replace("]", "").replace(".", "").replace('"', "").replace("?", "").replace("!", "").replace(",", ""))
            for word in datalist:
                listOfWords.append(word)

    return listOfWords

# This function makes a word cloud from a list of strings.
def makeWordcloud(wordlist):
    myCloud = wc.WordCloud()
    theCloud = myCloud.generate(' '.join(wordlist))
    plt.axis('off')
    plt.imshow(theCloud)

# These functions are courtesy of the DS2500 Canvas page.
# They are for finding magnitude of a vector...
def mag(v):
    return sum([i **2 for i in v]) ** 0.5

# ...the dot product of two vectors...
def dot(u, v):
    return sum([ui * vi for ui, vi in zip(u,v)])

# ...and the cosine similarity between two vectors.
def cossim(u, v):
    return (dot(u,v)/(mag(u) * mag(v)))

# Given a dictionary of words and word frequencies, and a list of words to
# look for in the dictionary, this will create a vector with elements
# corresponding to the value of the unique words in the dictionary.
def vectorCreator(wordDict, uniqueWords):
    vector = []
    for key, value in wordDict.items():
        if key in uniqueWords:
            vector.append(value)
            
    return vector

def main():
    # Create textfile variables
    shepardfile = 'shepard.txt'
    bartletfile = 'bartlet.txt'
    
    # Parse text files with functions
    shepardWords = listOfWords(shepardfile)
    bartletWords = listOfWords(bartletfile)
    shepardDict = Counter(shepardWords)
    bartletDict= Counter(bartletWords)
    
    # I'm not sure how this will tell us how the speeches are similar, as
    # these lists have no words in common, but I've picked 11 of the most
    # common unique words from each speech for vectors, taking "unique" to
    # mean that the word isn't a common word like "the", "a", "they", etc.
    sUniqueWords = ['bob', 'character', 'want', 'serious', 'bill', 'morning', 'white', 'house', 'rumson', 'president', 'country']
    bUniqueWords = ['children', 'poverty', 'five', 'code', 'today', 'first', 'time', 'history', 'largest', 'group', 'americans']
    
    shepardVector = vectorCreator(shepardDict, sUniqueWords)
    bartletVector = vectorCreator(bartletDict, bUniqueWords)
            
    print(cossim(shepardVector, bartletVector))
    
    # Cosine similarity of 0.867. My best interpretation of this is that the
    # frequency of distinct / unique words in the presidents' speeches follows
    # a similar curve, i.e. that the characters' speech is similar in terms of
    # how often they say particular, different distinct words. Neither
    # character uses unique words only once each, or overuses a particular
    # unique word.
    
    # Show word clouds.
    makeWordcloud(shepardWords)
    makeWordcloud(bartletWords)
    

main()