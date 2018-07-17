#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import psycopg2
import datetime
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math


def main():
    # Define our connection string
    conn_string = "host='pgteach' dbname='online_questions' user='s1617355' password='bayes123!' sslmode='disable'"

    # print the connection string we will use to connect
    print "Connecting to database\n ->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!\n"

    # conn.cursor
    cursor.execute("SELECT data FROM userdata;")

    data = cursor.fetchall()

    # Commit table
    conn.commit()

    # Close cursor
    cursor.close()

    # Close connection
    conn.close()

    return data

def toDate(timeStamp):
    return datetime.datetime.fromtimestamp(
        int(timeStamp/1e3)
    ).strftime('%Y-%m-%d %H:%M:%S')


def extract_game_choices():
    game_choices = []
    for i, participantData in enumerate(data):
        for entry in participantData:
            if entry["trial_type"] == "JMMcardgame":
                thrown_trials = len([t for t in entry["game_choices"] if len(t['cardsFlipped']) == 0])
                if thrown_trials > 10:
                    random_code = [e for e in participantData if e["trial_type"] == 'AJDrandom-code'][0]['randomCode']
                    print "More than 10 trials by participant thrown so results excluded. " \
                          "Number of trials thrown: %s. Turkers random code: %s" % (thrown_trials, random_code)
                    continue
                game_choices.extend(entry["game_choices"])
    return game_choices


if __name__ == "__main__":
    data = main()

    allGameChoices = extract_game_choices()
    multiplyTrials = [t for t in allGameChoices if t['criteria'] == 'Multiple']
    addTrials = [t for t in allGameChoices if t['criteria'] == 'Sum']
    numberedMultiplyTrials = {}
    numberedAddTrials = {}
    print 'Thrown Add trials: %s' % len([t for t in addTrials if len(t['cardsFlipped']) == 0])
    print 'Thrown Mult trials: %s' % len([t for t in multiplyTrials if len(t['cardsFlipped']) == 0])
    for i in range(1, 11):
        for t in addTrials:
            numberedAddTrials[i] = [t for t in addTrials if len(t['cardsFlipped']) > 0 and t['cards'][t['cardsFlipped'][0]]['value'] == i]
        for t in multiplyTrials:
            numberedMultiplyTrials[i] = [t for t in multiplyTrials if len(t['cardsFlipped']) > 0 and t['cards'][t['cardsFlipped'][0]]['value'] == i]

    numberedMultBiggestTrials = {}
    numberedMultSmallestTrials = {}
    numberedAddBiggestTrials = {}
    numberedAddSmallestTrials = {}
    for i in range(1, 11):
        numberedMultBiggestTrials[i] = [t for t in numberedMultiplyTrials[i] if t['direction'] == 'Biggest']
        numberedMultSmallestTrials[i] = [t for t in numberedMultiplyTrials[i] if t['direction'] == 'Smallest']
        numberedAddBiggestTrials[i] = [t for t in numberedAddTrials[i] if t['direction'] == 'Biggest']
        numberedAddSmallestTrials[i] = [t for t in numberedAddTrials[i] if t['direction'] == 'Smallest']
    biggestMultProbGuess = {}
    smallestMultProbGuess = {}
    biggestAddProbGuess = {}
    smallestAddProbGuess = {}
    for i in range(1, 11):
        biggestMultNumberGuessed = len([t for t in numberedMultBiggestTrials[i] if len(t['cardsFlipped']) == 1])
        biggestAddNumberGuessed = len([t for t in numberedAddBiggestTrials[i] if len(t['cardsFlipped']) == 1])
        biggestMultProbGuess[i] = biggestMultNumberGuessed/len(numberedMultBiggestTrials[i])
        biggestAddProbGuess[i] = biggestAddNumberGuessed/len(numberedAddBiggestTrials[i])
        smallestMultNumberGuessed = len([t for t in numberedMultSmallestTrials[i] if len(t['cardsFlipped']) == 1])
        smallestAddNumberGuessed = len([t for t in numberedAddSmallestTrials[i] if len(t['cardsFlipped']) == 1])
        smallestMultProbGuess[i] = smallestMultNumberGuessed/len(numberedMultSmallestTrials[i])
        smallestAddProbGuess[i] = smallestAddNumberGuessed/len(numberedAddSmallestTrials[i])

    biggestMultNumberVariance = {}
    biggestMultNumberVariance[1] = sum([(int(len(t['cardsFlipped']) == 1) - biggestMultProbGuess[1])**2 for t in numberedMultBiggestTrials[1]])
    # arrayOfValues = np.asarray([(int(len(t['cardsFlipped']) == 1)) for t in numberedMultBiggestTrials[6]])
    arrayOfValues = np.asarray([(int(len(t['cardsFlipped']) == 1)) for t in numberedMultSmallestTrials[7]])
    meanValue = np.mean(arrayOfValues)
    numpyVar = np.var(arrayOfValues)
    stdErrorOnMean = stats.sem(arrayOfValues)
    sem = math.sqrt(numpyVar/(len(arrayOfValues)))
    print 'Std error on mean scipy: %s, Std error on mean ours: %s' % (stdErrorOnMean, sem)
    print 'My mean: %s. Numpy mean: %s' % (biggestMultProbGuess[1], meanValue)
    print 'My variance: %s. Numpy variance: %s' % (biggestMultNumberVariance[1], numpyVar)

    multBias = 0.0
    addBias = 0.0
    multBiasDict = {}
    addBiasDict = {}
    for i in range(6, 11):
        multBias += (biggestMultProbGuess[i] - smallestMultProbGuess[i])
        addBias += (biggestAddProbGuess[i] - smallestAddProbGuess[i])
    for i in range(1, 6):
        multBias += (smallestMultProbGuess[i] - biggestMultProbGuess[i])
        addBias += (smallestAddProbGuess[i] - biggestAddProbGuess[i])
    for i in range(1, 11):
        multBiasDict[i] = biggestMultProbGuess[i] - smallestMultProbGuess[i]
        addBiasDict[i] = biggestAddProbGuess[i] - smallestAddProbGuess[i]


    print 'Positive Evidence Approach Bias Multiply: %s' % multBias
    print 'Positive Evidence Approach Bias Sum: %s' % addBias
    plotChoice = 'mult'
    if plotChoice == 'mult':
        plt.plot(biggestMultProbGuess.keys(), biggestMultProbGuess.values(), marker='.', markersize=15)
        plt.plot(smallestMultProbGuess.keys(), smallestMultProbGuess.values(), marker='.', markersize=15)
        plt.legend(['Biggest Multiple', 'Smallest Multiple'], loc='upper right')
        plt.axis([0.8, 10.5, 0.0, 1.0])
        plt.xlabel('First Card Value')
        plt.ylabel('Probability of Guessing')
        plt.title('Behaviour: Multiply Trials')
        plt.xticks(np.arange(1, 11, 1.0))
        plt.show()
    elif plotChoice == 'add':
        plt.plot(biggestAddProbGuess.keys(), biggestAddProbGuess.values(), marker='.', markersize=15)
        plt.plot(smallestAddProbGuess.keys(), smallestAddProbGuess.values(), marker='.', markersize=15)
        plt.legend(['Biggest Sum', 'Smallest Sum'], loc='upper right')
        plt.axis([0.8, 10.5, 0.0, 1.0])
        plt.xlabel('First Card Value')
        plt.ylabel('Probability of Guessing')
        plt.title('Behaviour: Add Trials')
        plt.xticks(np.arange(1, 11, 1.0))
        plt.show()
    elif plotChoice == 'diff':
        plt.plot(multBiasDict.keys(), multBiasDict.values(), marker='.', markersize=15)
        plt.plot(addBiasDict.keys(), addBiasDict.values(), marker='.', markersize=15)
        plt.legend(['Multiple', 'Sum'], loc='upper right')
        plt.xlabel('First Card Value')
        plt.ylabel('Relative Probability of Guessing')
        plt.title('Positive Evidence Approach: Biggest Minus Smallest')
        plt.show()
