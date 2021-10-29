#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 14:00:48 2021

Student: Connor Brown
Date: 09/26/21
Project: Week 1 Homework (Board Games)
"""

# Neccesary imports
import math
import matplotlib.pyplot as plt
import numpy as np

# Part A: Create a dictionary of all game data
def fillDict(csvfile):
    
    # Initialize dictionary to be filled
    games_dict = {}
    
    # Read in data from CSV
    with open(csvfile, "r") as textfile:
        for r in textfile:
            datalist = r.split(",")
            
            # Only add data to dictionary if it can be single-player
            if datalist[1] == "1":
                # Formatting for the nested dictionary
                games_dict[datalist[0]] = {"minplaytime": float(datalist[2]), \
                                      "maxplaytime": float(datalist[3]), \
                                          "minage": float(datalist[4]), \
                                              "average": float(datalist[5]), \
                                                  "avgweight": \
                                                      float(datalist[6])}
            
    return games_dict

# Part B: This function will compare one game to another and return their
# Euclidean distance.
def compareGames(game1, game2, games_dict):
    
    total = 0
    
    # Iterate through all measurements of the board games
    values = ['minplaytime', 'maxplaytime', 'minage', 'average', 'avgweight']
    for value in values:
        
        # The Euclidean distance metric 🤓
        # First, subtract one value from the other
        val1 = games_dict[game1][value] - games_dict[game2][value]
        # Second, square this value
        val1 = val1**2
        # Third, add all the values together
        total += val1
    # Finally, take the square root of this sum
    return math.sqrt(total)

# Part B: This function will come up with a reccomendation for a given game
# based on the dictionary of all board games
def recommendation(game1, games_dict):
    
    # Set up variables for the recommended game and distance between your
    # game and that game, which will be replaced later.
    bestGame = ''
    distance = 999999999
    
    
    for game in games_dict:
        # Make sure you don't end up reccomending the same game...
        if game != game1:
            # Use earlier function with every other game in the list
            distanceFromCurrent = compareGames(game1, game, games_dict)
            # Replace recommended game if its Euclidean distance is smallest
            if distanceFromCurrent < distance:
                distance = distanceFromCurrent
                bestGame = game
                
    return bestGame

# Part C: This function will return all data neccesary for constructing
# our two plots when parametrized with the dictionary of our game data
def gatherPlotData(games_dict):
    
    # For the first bar chart, showing how many games are rated at each integer
    ratingQuantities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    # For the second chart, plotting ratings against weights
    gameRatings = []
    gameDifficulties = []
    
    for game, info in games_dict.items():
        # I'm proud of this one - increment the value in the list which is
        # indexed at the value of the rounded rating. e.g. if the first game
        # that we look at is rated 7.9, the list looks like this:
        # [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        ratingQuantities[round(info['average'])] += 1
        
        # Append data from dictionaries to lists so they match up indexwise
        gameRatings.append(info['average'])
        gameDifficulties.append(info['avgweight'])
    
    # Create the x-axis labels for the rating quantity chart
    x_labels = [str(i) for i in range(10)]
    
    return ratingQuantities, x_labels, gameRatings, gameDifficulties
        
def main():
    
    # Execute Part A
    games = fillDict("bgg.csv")
    
    # Execute Part B
    yourGame= 'Mage Knight Board Game'
    rec = recommendation(yourGame, games)
    print("Since you like " + yourGame + ", you'll love " + rec + "!")
    
    # Execute Part C
    rateQuants, ratings, allRatings, allWeights = gatherPlotData(games)
    
    # First Plot: Number of Ratings of a Given Integer Value
    plt.bar(ratings, rateQuants)
    plt.xlabel('Rating')
    plt.ylabel('Number of Board Games')
    plt.title('Single-Player Board Game Ratings')
    
    # Draw First Plot
    plt.show()
    
    # Second Plot: Game Rating vs. Game Weight
    plt.scatter(allWeights, allRatings, s=4)
    plt.xlabel('Game Weight')
    plt.ylabel('Game Rating')
    # plt.ylim([0, 5])
    plt.title('Game Rating vs. Game Weight')
    
    # Create line of best fit to see correlation
    x = np.array(allWeights)
    y = np.array(allRatings)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b, color = "red")
    
    # Indicate obvious outliers (they're still included in the line of best
    # fit, but c'est la vie)
    plt.text(0.5, 0.4, "Games with weight 0 have not had their weight rated.")
    
    # Draw Second Plot
    plt.draw()

    """
    Part D. Business Marketing Thought Question
    
    Based on the plot and the information from the PDF, I would reccomend a 
    target weight of about 2.8 - 3. Although the correlation implies that
    game ratings tend to increase with weight, which would increase sales,
    it appears that the maximally-fun games are somewhere between 1.5 and 3.2
    in weight. If I'm a "head of marketing for a boardgame company wishing to
    break into the solo board gaming arena", I would want to trust the team
    making the game, and tell them to make a game of about that difficulty. Of
    note is the fact that there exists a game in the mid 3s in terms of weight,
    which no higher-weighted game is able to surpass in rating. I'd like to
    think that the team at my company would make that type of game!
    """
    
main()

