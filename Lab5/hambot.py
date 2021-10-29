#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 20:21:10 2021

@author: cabrown802
"""

#Neccesary imports and printing options
import numpy as np
import sys
import random
np.set_printoptions(threshold=sys.maxsize)

# A function that removes blank values from a sequence
def removeBlanks(numpyArray):
    for element in range(len(numpyArray)):
        try:
            if len(numpyArray[element]) == 0:
                numpyArray = np.delete(numpyArray, element)
                element -= 1
        except IndexError:
            pass
        
    return numpyArray

# Neccesary variable declarations
statfile = 'hamilton_lyrics.txt'
rows = np.array('')
words = np.array('')
firstwords = np.array('')
lastwords = np.array('')

# Read rows of txt file into "rows" array
with open(statfile, "r") as textfile:
    for r in textfile:
        rows = np.append(rows, r)

# Citation for translation table used to remove certain characters from words:
# https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
translation_table = dict.fromkeys(map(ord, ',!.?—:…()"“'), None)

# Add words to arrays of words, firstwords, and lastwords.
for row in rows:
    # For each line of dialogue, split it into a list on the spaces
    split = row.split(" ")
    # Index variable used for finding first and last words.
    # Non-Pythonic for sure, but very useful!
    index = 0
    # Iterate over each word
    for word in split:
        # Iterate index
        index += 1
        # Check if the word is not a header / speaker indication
        if '[' not in word and ']' not in word:
            # Add first words to firstwordd
            if index == 1:
                if word != '\n':
                    firstwords = np.append(firstwords, word.lower().rstrip().translate(translation_table))
            # Add last words to lastwords
            if index + 1 == len(split) + 1:
                if len(word) > 1 or word.lower() == 'i' or word.lower() == 'a':
                    lastwords = np.append(lastwords, word.lower().translate(translation_table).rstrip())
            # Add all words to words
            words = np.append(words, word.lower().translate(translation_table).rstrip())

# Remove any blank entries that the above process didn't take care of
firstwords = removeBlanks(firstwords)
lastwords = removeBlanks(lastwords)
words = removeBlanks(words)

#import pdb; pdb.set_trace()

# Create dictionary with each word in Hamilton as keys and empty list as values
# These lists will soon contain each word following the keyword in the script
two_grams = d = {key: [] for key in words}

# Initialize a list of words which have already been dictionarily two-grammed
dupls = []

# For EVERY WORD
for word in words:
    # If it's not a duplicate or somehow still a blank value,
    if word not in dupls and len(word.rstrip()) > 0:
        # Add the word to the list of duplicates
        dupls.append(word)
        # List comprehension: grab indicies of all cases in which the word
        # appears. enumerate() is super helpful here
        indices = [p for p, x in enumerate(words) if x == word]
        # For each index that the word appears, try to append the word after it
        # to the corresponding list inside of our dictionary
        for oneindex in indices:
            try:
                # Don't add duplicates!
                if words[oneindex + 1] not in two_grams[word]:
                    two_grams[word].append(words[oneindex + 1])
            except IndexError:
                continue

# Remove blank values in dictionary
for key, value in two_grams.items():
    value = removeBlanks(value)

def main():
    
    # Number of sentences to make
    looper = int(input("How many sentences would you like to print? "))
    
    # Repeat sentence-production process looper times
    for i in range(looper):
        
        # Choose a random word from our list
        firstWord = random.choice(words)
        # Add that word to our sentence
        sentence = [firstWord]
        
        # Until we reach a word in lastwords, come up with a random nextWord
        # from the corresponding list inside of our dictionary for our
        # firstWord. Then set the new "firstWord" to this word and loop.
        while(True):
            nextWord = random.choice(two_grams[firstWord])
            sentence.append(nextWord)
            if nextWord in lastwords:
                break
            else:
                firstWord = nextWord
                
        # Print the sentence!
        print(sentence)
        # Note to grader: because our stopwords are so numerous and include
        # frequently used words like 'to' and 'on', most "sentences" are short.
        
main()

# print(len(firstwords))
# print(len(lastwords))
# I don't know why these values ^ differ :(