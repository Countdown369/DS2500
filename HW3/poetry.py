#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 12:28:24 2021

@author: cabrown802
"""

import wordcloud as wc
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob
import seaborn as sns
import pandas as pd
import numpy as np
import math

# This function takes in a text file and returns a list of each word in the
# file, removing punctuation. This is my code, copied from my Week 7 Lab,
# edited so that punctuation can be optionally included (punc = True) or not,
# and so that it can optionally read full lines instead of single words
# (lines = True) for sentiment analysis
def listOfWords(txt, punc, lines):
    listOfWords = []
    with open(txt, "r") as textfile:
        if lines:
            for r in textfile:
                listOfWords.append(r.strip())
            return listOfWords
        else:
            for r in textfile:       
                datalist0 = r.split(" ")
                datalist = []
                for i in range(len(datalist0)):
                    datalist0[i] = datalist0[i].strip()
                    
                for i in range(len(datalist0)):
                    if punc:
                        continue
                    else:
                        try:
                            datalist0[i] = datalist0[i].lower()
                        except:
                            datalist[i] = ""
                for word in datalist0:
                    if len(word) > 0:
                        if punc:
                            datalist.append(word)
                        else:
                            datalist.append(word.replace("[", "").replace("]", "").replace(".", "").replace('"', "").replace("?", "").replace("!", "").replace(",", ""))
                for word in datalist:
                    listOfWords.append(word)

    return listOfWords

# This function makes a word cloud from a list of strings. Also taken from my
# Week 7 lab.
def makeWordcloud(wordlist, disclude):
    myCloud = wc.WordCloud(stopwords = list(wc.STOPWORDS) + disclude)
    theCloud = myCloud.generate(' '.join(wordlist))
    plt.axis('off')
    plt.imshow(theCloud)
    plt.draw()
    plt.clf()
    # After some googling, it seems like it may be impossible to show all
    # wordclouds using the loop of this function in the next function.
    # Apparently I need to use something called openCV or waitkey?
    
# Uses makeWordcloud() to make wordclouds of all elements of a list.
def makeAllClouds(anotherlist):
    for wordlist in anotherlist:
        makeWordcloud(wordlist, ["s"])

# Edited from the class file "twitter_sentiment.py"
def scorePoems(poems, minsub=0.0, maxsub=1.0, minpol=-1.0, maxpol=1.0):
    filtered = {}
    index = 0
    for poem in poems:
        pol, sub = TextBlob(poem).sentiment
        if minpol <= pol <= maxpol and minsub <= sub <= maxsub:
            filtered[str(index)] = (pol, sub)
        index += 1
    return filtered

# Plot subjectivity and polarity of ENTIRE poems
def fullPoemPlots(quantity, fullSentiments):
    x = ["Kennedy", "Clinton 1", "Clinton 2", "Obama 1", "Obama 2", "Biden"]
    y= []
    for pol_dict in fullSentiments.values():
        y.append(pol_dict[quantity])
    plt.scatter(x,y)
    plt.title("(Sentiment Analysis Performed on Entire Poem)")
    plt.xlabel("Address")
    if quantity == 0:
        plt.ylabel("Polarity")
        plt.suptitle("Polarity of Presidential Inaugural Poems (1961 - 2021)")
    if quantity == 1:
        plt.ylabel("Subjectivity")
        plt.suptitle("Subjectivity of Presidential Inaugural Poems (1961 - 2021)")
    plt.draw()

# Used for plotting subjectivity and polarity in a by-line fashion. Takes list
# of dictionaries and wrangles this data into a dataframe.
def wrangle(myList):
    apbl = pd.DataFrame(columns=["Poem", "Line", "Polarity", "Subjectivity"])
    poems = ["Kennedy", "Clinton 1", "Clinton 2", "Obama 1", "Obama 2", "Biden"]
    poemindex = 0
    for dictionary in myList:
        lineindex = 1
        for polcommasub in dictionary.values():
            apbl.loc[len(apbl.index)] = [poems[poemindex], lineindex, polcommasub[0], polcommasub[1]]
            lineindex += 1
        poemindex += 1
    return apbl

# Generate sentiments for lines of poem
def lineSentiments(linelists):
    bylineSentiments = []

    for seperatedPoem in linelists:
        bylineSentiments.append(scorePoems(seperatedPoem))
    
    return bylineSentiments

# Plot subjectivity and polarity of poems, analyzing each line individually.
def bylinePoemPlots(apbl, measure):
    sns.set(style="ticks", font_scale=3, rc={"lines.linewidth": 1, "xtick.labelsize": 0})
    if measure == "Polarity":
        g = sns.FacetGrid(apbl, col="Poem", col_wrap=6, height=8, ylim=(-1, 1))
    elif measure == "Subjectivity":
        g = sns.FacetGrid(apbl, col="Poem", col_wrap=6, height=8, ylim=(0, 1))
    else:
        return None
    g.map(sns.pointplot, "Line", measure, order = [i for i in range(120)], color=".3", ci=None)

# These functions are, again, courtesy of the DS2500 Canvas page.
# They are for finding magnitude of a vector...
def mag(v):
    return sum([i **2 for i in v]) ** 0.5

# ...the dot product of two vectors...
def dot(u, v):
    return sum([ui * vi for ui, vi in zip(u,v)])

# ...and the cosine similarity between two vectors.
def cossim(u, v):
    return (dot(u,v)/(mag(u) * mag(v)))

# Euclidean distance metric for vectors in R^n
def euclidean(u, v):
    thesum = 0
    for i in range(len(u)):
        thesum += (abs(u[i] - v[i]))**2
    return math.sqrt(thesum)
        
# Turns top 10 most common words in each poem into frequency vectors in R^10
def vectorize(lowerlists):
    vectors = []
    for listowords in lowerlists:
        vector = []
        topwords = pd.DataFrame.from_dict(Counter(listowords), orient='index').reset_index()
        topwords = topwords.sort_values([0], ascending=[False])
        index = 0
        for key, value in topwords.iterrows():
            if index > 9:
                break
            vector.append(value.to_numpy()[1])
            index += 1
        vectors.append(vector)
    return vectors

# Creates plots concerning the comparison of repition across poems
def plotCommonWordFrequency(cosines, euclideans, cotitle, eutitle, labels):
    sns.set(style="ticks", font_scale=1, rc={"lines.linewidth": 1, "xtick.labelsize": 10})
    eu = sns.heatmap(euclideans, xticklabels = labels, yticklabels = labels, cmap = sns.cm.rocket)
    plt.title(eutitle)
    plt.show()
    plt.clf()
    plt.title(cotitle)
    co = sns.heatmap(cosines, xticklabels = labels, yticklabels = labels, cmap = sns.cm.rocket_r)
    plt.show()
    plt.clf()

# A simple plot which shows how long poems are
def plotPoemLengths(line_nums):
    sns.set(style="ticks", font_scale=1, rc={"lines.linewidth": 1, "xtick.labelsize": 10})
    plotx = ["Kennedy", "Clinton 1", "Clinton 2", "Obama 1", "Obama 2", "Biden"]
    plt.scatter(plotx, line_nums)
    plt.xticks(ticks = [i for i in range(6)], labels = plotx)
    plt.title("Length of Presidential Poems (by number of lines)")
    plt.xlabel("Address")
    plt.ylabel("Number of Lines")

# Scale word frequency vectors inversely by the length of the poem
def normVectors(vectors, lowerlists):
    normedVectors = []
    for i in range(len(vectors)):
        nv = []
        for j in range(len(vectors[i])):
            nv.append(vectors[i][j] / len(lowerlists[i]))
        normedVectors.append(nv)
    return normedVectors

# Does what it says on the tin, I mean c'mon
# (Creates arrays which are then plotted in heatmaps)
def constructHeatmapArrays(vectors, normedVectors):
    cosines = np.zeros((6,6))
    euclideans = np.zeros((6,6))
    for i in range(6):
        for j in range(6):
            cosines[i][j] = cossim(vectors[i], vectors[j])
            euclideans[i][j] = euclidean(normedVectors[i], normedVectors[j])
    return cosines, euclideans

# Creates the basic lists which are used for data analysis in main()
def makeDataLists(files):
    lowerlists = []
    punclists = []
    linelists = []
    for file in files:
        lowerlists.append(listOfWords(file, False, False))
        punclists.append(listOfWords(file, True, False))
        linelists.append(listOfWords(file, False, True))
    return lowerlists, punclists, linelists

# Count lines of poems in a list of poems
def countLines(files):
    line_nums = []
    for file in files:
        num_lines = sum(1 for line in open(file))
        line_nums.append(num_lines)
    return line_nums

# Get data about number of punctuation characters per poem
def getPuncData(longpuncstrings):
    question = []
    exclamation = []
    dash = []
    comma = []

    for strig in longpuncstrings:
        question.append(Counter(strig)["?"])
        exclamation.append(Counter(strig)["!"])
        dash.append((Counter(strig)["-"]) + (Counter(strig)["—"]))
        comma.append(Counter(strig)[","])
        
    return question, exclamation, dash, comma

# Make strings of entire poem
def makeLongs(lowerlists, punclists):
    longstrings = []
    longpuncstrings = []
    for lists in lowerlists:
        longstrings.append(' '.join(lists))
    for lists in punclists:
        longpuncstrings.append(' '.join(lists))
    return longstrings, longpuncstrings


# Plot number of punctuation marks per poem
def plotPunctuation(question, exclamation, dash, comma, xtfs):
    plt.clf()
    x = ["Kennedy", "Clinton 1", "Clinton 2", "Obama 1", "Obama 2", "Biden"]
    y1 = question
    y2 = exclamation
    y3 = dash
    y4 = comma
    
    plt.figure()
    plt.subplot(3,2,1)
    plt.plot(x,y1,'ro')
    plt.title("Question Marks per Poem")
    plt.yticks(ticks = [0, 1, 2, 3, 4])
    plt.xticks(fontsize=xtfs, rotation = 80)
    
    plt.subplot(3,2,2)
    plt.plot(x,y2,'ro')
    plt.title("Exclamation Points per Poem")
    plt.xticks(fontsize=xtfs, rotation = 80)
    plt.yticks(ticks = [0])
    
    plt.subplot(3,2,5)
    plt.plot(x,y3,'ro')
    plt.title("Dashes per Poem")
    plt.xticks(fontsize=xtfs, rotation = 80)
    plt.yticks(ticks = [0, 6, 12])
    
    plt.subplot(3,2,6)
    plt.plot(x,y4,'ro')
    plt.title("Commas per Poem")
    plt.xticks(fontsize=xtfs, rotation = 80)
    plt.yticks(ticks = [0, 25, 50, 75, 100])
               
    plt.show()

def main():
    # Setup vars
    kennedyf = 'kennedy.txt'
    clinton1f = 'clinton1.txt'
    clinton2f = 'clinton2.txt'
    obama1f = 'obama1.txt'
    obama2f = 'obama2.txt'
    bidenf = 'biden.txt'
    
    files = [kennedyf, clinton1f, clinton2f, obama1f, obama2f, bidenf]
    
    # Create lists of words to do data analysis on
    # (list of lowercase words, list of words with punctuation, list of lines)
    lowerlists, punclists, linelists = makeDataLists(files)
    
    # Create list of strings, which strings contain the entire lowercase poem
    # and strings which contain the entire poem with punctuation
    longstrings, longpuncstrings = makeLongs(lowerlists, punclists)
    
    # Take sentiments of full poems and lines of poems
    fullSentiments = scorePoems(longstrings)    
    bylineSentiments = lineSentiments(linelists)
    
    # Wrangle data for by-line sentiment graph
    apbl = wrangle(bylineSentiments)
    
    # Make vectors of top 10 words per poem, and compare them to each other
    vectors = vectorize(lowerlists)
    normedVectors = normVectors(vectors, lowerlists)
    cosines, euclideans = constructHeatmapArrays(vectors, normedVectors)
    
    # Create line numbering data
    line_nums = countLines(files)
    
    # Create punctuation data
    question, exclamation, dash, comma = getPuncData(longpuncstrings)
    
    # ----------------------------------------------------------------------
    
    # Plots, content of which should be evident based on the function names.
    
    # Because I still need to figure out how seaborn and plt interact, and how
    # to properly draw then CLOSE a plot (or figure? or axes?), please only
    # run one plot at a time. My computer can execute the entire program in ~5
    # seconds, so this shouldn't be a HUGE problem if you want to generate the
    # plots yourself. 
    
    # Still annoying. Sorry about that. I'll look into it.
    
    # makeAllClouds(lowerlists)
    
    # fullPoemPlots(0, fullSentiments)
    # fullPoemPlots(1, fullSentiments)
    
    # bylinePoemPlots(apbl, "Polarity")
    # bylinePoemPlots(apbl, "Subjectivity")
    
    # plotCommonWordFrequency(cosines, euclideans, "Cosine Similarity Between Freuqency of Most Common Words in Poems", "Euclidean Distance Between Freuqency of Most Common Words in Poems", ["Kennedy", "Clinton 1", "Clinton 2", "Obama 1", "Obama 2", "Biden"])
    
    # plotPoemLengths(line_nums)
    
    # plotPunctuation(question, exclamation, dash, comma, 12)
    
main()