#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 11:40:13 2021

Student: Connor Brown
Date: 09/23/21
Project: Week 3 Lab (Tic-Tac-Toe)
"""

# Neccesary imports
import random
import numpy as np

# This function will make a random board of a specified dimension,
# and print the board if wanted.
def makeRandomBoard(dimen, printing):
    # Parameters:
        # dimen: dimension of the square two-dimensional numpy array
        # printing: True if you want the board to be printed, False otherwise
    
    # Fill a board of specified dimension with zeros
    board = np.zeros((dimen,dimen))
    
    """
    In my game, untouched spaces are represented by 0,
    X'd spaces are represented by 1, and
    O'd spaces are represented by pi (np.pi, specifically).
    These numbers are later converted into X's and O's for printing.
    
    After researching co-prime numbers, linear combinations, and eventually
    settling for just setting one of the numbers to a really high number,
    I spoke with my linear algebra professor about how to ensure that
    the sum of elements of a row, column or diagonal would never sum to
    (that number) * (dimension of the board). I had been running into issues
    where, with small numbers, setting a board dimension of ~1000 would always
    result in a win, since it was just likely to occur based on the probability
    that one of the ~2002 rows, columns, and diagonals would sum to the sum
    of one of my chosen numbers or the other. (If you want to see what I mean,
    change the 1 and np.pi below to 3 and 7, and make a 1000x1000 board.)
    
    My professor rold me that this would be impossible with rational numbers,
    as you could always multiply the lesser one by an integer to get a multiple
    of the greater one. Instead, I have to use irrational numbers.
    Theoretically, any irrational number for 'O's and any rational number for 
    'X's (or vice versa) should work -- now I just hope that:
    a) np.pi is actually a Wolfram-style irrational number on a computer,
    and not just a really good approximation, and
    b) that if a) fails, that nobody will type in a number high enough to cause
    these collisions.
    
    This result is the best version I was able to create specifically to ensure
    that sum() collisions would not occur. Here's to hoping it works. Be good,
    np.pi.
    """
    
    # Choosing from possible moves (equally), loop through every board space.
    
    moves = [0, 1, np.pi]
    
    for q in range(dimen):
        for w in range(dimen):
            board[q][w] = random.choice(moves)
    
    # Print, if printing.
    if printing:
        
        """
        I tried doing this originally by converting the actual board to a list,
        then converting that list back to an ndarray. Don't do that. You can
        just make a new variable. You already knew this, this is mostly a note
        to myself.
        """
        
        # Make a board that you will print:
        # Make it so you can change it into storing different types by making
        # it a list
        board2 = list(board)
        
        # For every element in the board, check its value and change it
        for i in range(dimen):
            
            # Remember that now we just have a list that contains ndarrays.
            # Let's convert these into lists, too.
            board2[i] = list(board2[i])
            
            for j in range(dimen):
    
                if board2[i][j] == 1:
                    board2[i][j] = 'X'
                if board2[i][j] == np.pi:
                    board2[i][j] = 'O'
                if board2[i][j] == 0:
                    board2[i][j] = '-'
        
        # Print rows one at a time.
        for rows in board2:
            print(rows)
        
    return(board)

# This function will test a given board and return a string of the winner.
# If there is no winner, it will return "NO WIN"
def testBoard(xo_board):
    
    # Printing a new line here makes output look cleaner
    print()
    
    # This 'done' variable will be returned at the end.
    # It keeps track of complete O and X rows, columns, and diagonals.
    # Every time a player gets one, their letter is added to the string.
    done = ''
    
    # Make a list that will contain column entries so that we can use sum()
    colList = []
    
    # First, test rows.
    for i in range(len(xo_board)):
        
        # If a row sum is the 3 * dimension of the array squared, X wins.
        if sum(xo_board[i]) == len(xo_board):
            print("X wins!")
            done += 'X'
            
        # If a row sum is 7 * the dimension of the array squared, O wins.
        elif sum(xo_board[i]) == len(xo_board) * np.pi:
            print("O wins!")
            # Add 'O' to the string of wins
            done += 'O'

        # This ensures a clear column list for each column we check.
        colList.clear()
        
        # Then, check by column.
        for j in range(len(xo_board)):
            # Append column entries to list
            colList.append(xo_board[j][i])
            
            if sum(colList) == len(xo_board):
                print("X wins!")
                done += 'X'

            elif sum(colList) == len(xo_board) * np.pi:
                print("O wins!")
                done += 'O'
                
    # Similar implementation for diagonals as for columns;
    # make a list to use sum() on.
    diagList = []
    
    # By now, one may be able to look at the above logic
    # and see how it is similarly applied to diagonal entires.
    
    # This first k loop checks \ diagonals.
    for k in range(len(xo_board)):
        diagList.append(xo_board[k][k])
        if sum(diagList) == len(xo_board):
            print("X wins!")
            done += 'X'
        elif sum(diagList) == len(xo_board) * np.pi:
            print("O wins!")
            done += 'O'
        
        if done:
            return done
    
    # If that didn't work, finally check / diagonals.
    diagList.clear()
    
    for h in range(len(xo_board)):
        
        # This ugly indexing allows for scaling the diagonal in the / way
        # Take the board dimension, subtract one, then subtract h,
        # and you get the "complement" of h in terms of dimension of the board.
        diagList.append(xo_board[len(xo_board)-h-1][h])
        if sum(diagList) == len(xo_board):
            print("X wins!")
            done += 'X'
        elif sum(diagList) == len(xo_board) * np.pi:
            print("O wins!")
            done += 'O'
    
    # If there was more than one win, and both players have at least one,
    # with the way the program is made, there is no way to see who would have
    # won "first". I'm okay with this, but it does require this draw rule
    # where any shared victories result in a draw. I think this is fair.
    if len(done) > 1:
        record = list(done)
        if 'O' in record and 'X' in record:
            return 'DRAW'
        elif 'O' in record:
            return 'O'
        else:
            return 'X'
        
    elif len(done) == 1:
            return done
    
    # If nothing has returned by this point, then no row, column, or diagonal
    # is winning. Return "DRAW".
    else:
        print("DRAW")
        return "DRAW"

def main():
    
    # Ask the user how many simulations they want to test, and the dimension
    # of the boards in this simulation.
    print("\nYou are about to run a simulation of tic-tac-toe.")
    
    testNum = int(input("How many games do you want the computer to play? "))

    dimension = int(input("How big should the boards be? "))
    
    print()
    
    # Execute functions.
    for whoCaresWhatThisIteratorIsCalledReally in range(testNum):
        testBoard(makeRandomBoard(dimension, True))
        print()
        
main()