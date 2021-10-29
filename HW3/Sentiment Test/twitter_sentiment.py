#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    DS2500
    Spring 2021
    Sample code from class -- sentiment analysis of 2020 election tweets
    Two data files -- tweets w/tag #joebiden, and tweets w/tag #donaldtrump
    
    To install the textblobl module...
    
    From terminal (Mac):
        conda install -c conda-forge textblob
        
    Windows users: 
        right-click Anaconda Prompt
        in start window and select More...Run as administrator
        
    From Anaconda Navigator:
    1. Go to environments
    2. Select base environment
    3. Select channels
    4. Add....conda-forge
    5. Update channels
    6. Search for textblob
    7. Select for installation
    8. Click Apply


"""

"""
POLARITY: -1 (Very Negative) to +1 (Very Positive)
SUBJECTIVITY: 0.0 (Very Objective) to 1.0 (Very Subjective)
"""



import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob


    

#%%
def read_tweets(filename):
    ''' Function: read_tweet_csv
        Parameters: name of .csv file (string)
        Returns: list of tweet text (strings)
    '''
    with open(filename) as infile:
        tweets = infile.readlines()
        tweets = [tweet.strip() for tweet in tweets]
    return tweets


#%% Filtered tweets

def score_tweets(tweets, minsub=0.0, maxsub=1.0, minpol=-1.0, maxpol=1.0):
    filtered = {}
    index = 0
    for tweet in tweets:
        if index == 0:
            import pdb; pdb.set_trace()
        pol, sub = TextBlob(tweet).sentiment
        if minpol <= pol <= maxpol and minsub <= sub <= maxsub:
            filtered[tweet] = (pol, sub)
    return filtered
    

#%% Polarity vs Subjectivity distribution

def polarity_vs_subjectivity(scored_tweets, title='', marker='black'):
    scores = scored_tweets.values()
    polarity = [x[0] for x in scores]
    subjectivity = [x[1] for x in scores]
    
    fig = plt.figure(figsize=(10,10), dpi=100)
    plt.xlabel('Subjectivity')
    plt.ylabel('Polarity')
    plt.title(title+': Sentiment analysis')

    sns.scatterplot(x=subjectivity, y=polarity, s=3, color=marker)
    sns.kdeplot(x=subjectivity, y=polarity, color='black')
    plt.show()
    

#%%

def main():
    
    trump_tweets = read_tweets('hashtag_donaldtrump.csv')
    scored_trump_tweets = score_tweets(trump_tweets)
    polarity_vs_subjectivity(scored_trump_tweets, title = 'Trump', marker='red')

    biden_tweets = read_tweets('hashtag_joebiden.csv')
    scored_biden_tweets = score_tweets(biden_tweets)
    polarity_vs_subjectivity(scored_biden_tweets, title = 'Biden', marker='blue')    

    
    
if __name__ == '__main__':
    main()
    
    
    

    
        
    
        
    
    