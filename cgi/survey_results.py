#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import psycopg2
import numpy as np
import os
import json
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import ast

OPTIONS_ALTMAN = [
    ['I do not feel happier or more cheerful than usual.', 
    'I occasionally feel happier or more cheerful than usual.', 
    'I often feel happier or more cheerful than usual.', 
    'I feel happier or more cheerful than usual most of the time.', 
    'I feel happier or more cheerful than usual all of the time.'],
    ['I do not feel more self-confident than usual.', 
    'I occasionally feel more self-confident than usual.', 
    'I often feel more self-confident than usual.',  
    'I feel more self-confident than usual.', 
    'I feel extremely self-confident all of the time.'],
    ['I do not need less sleep than usual.', 
    'I occasionally need less sleep than usual.', 
    'I often need less sleep than usual.', 
    'I frequently need less sleep than usual.', 
    'I can go all day and night without any sleep and still not feel tired.'],
    ['I do not talk more than usual.', 
    'I occasionally talk more than usual.', 
    'I often talk more than usual.', 
    'I frequently talk more than usual.', 
    'I talk constantly and cannot be interrupted.'],
    ['I have not been more active (either socially, sexually, at work, home or school) than usual.', 
    'I have occasionally been more active than/ usual.', 
    'I have often been more active than usual.', 
    'I have frequently been more active than usual.', 
    'I am constantly active or on the go all the time.']
]

OPTIONS_PHQ = [
    ['Not at all','Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all','Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all','Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all','Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all','Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all','Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all','Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all','Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all','Several days', 'More than half the days', 'Nearly every day'],
    ['Not difficult at all', 'Somewhat difficult', 'Very difficult', 'Extremely difficult']
]

OPTIONS_LOTR = [
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"],
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"],
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"],
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"],
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"],
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"],
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"],
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"],
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"],
    ["I agree a lot", "I agree a little","I neither agree nor disagree","I disagree a little","I disagree a lot"]
]


def getData():

    #Define our connection string
    conn_string = "host='pgteach' dbname='online_questions' user='s1617355' password='bayes123!' sslmode='disable'"
 
    # print the connection string we will use to connect
    print "Connecting to database\n ->%s" % (conn_string)
 
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!\n"

    # conn.cursor
    cursor.execute("SELECT data FROM userdata where Id > 35;")

    data = cursor.fetchall()

    # Commit table
    conn.commit()

    # Close cursor
    cursor.close()

    # Close connection
    conn.close()

    return data

def surveyData(participantID, questionID, surveyAnswers, dictSurveys):
    count = 0
    for k, v in surveyAnswers.iteritems():
        # LOT-R
        if questionID == 18:
            idx = OPTIONS_LOTR[int(k[1])].index(v)
            count += idx
        # SPQ-B
        elif questionID == 19:
            if v == "Yes":
                count += 1
        # ALTMAN
        elif questionID == 20:
            idx = OPTIONS_ALTMAN[int(k[1])].index(v)
            count += idx
        # PHQ-9
        elif questionID == 21:
            if int(k[1]) == 9:
                pass
            else:
                idx = OPTIONS_PHQ[int(k[1])].index(v)
                count += idx


    addToSurveyDict(dictSurveys, questionID, count)

def addToSurveyDict(dictionary, key, entry):
    if key not in dictionary:
        dictionary[key] = [entry]
    else:
        dictionary[key].append(entry)

def get_survey_dict():
    # dictionary has keys 1...numParticipants and arrays of survey results
    dictSurveys = {}
    data = getData()
    data = [entry[0] for entry in data]
    for i, participantData in enumerate(data):
        for entry in participantData:

            # Get the node ID
            nodes = [int(float(val)) for val in entry["internal_node_id"].split("-")]

            # Get the survey results for each participant
            if len(nodes) != 3 and entry["trial_type"] == "AJDsurvey":
                _, questionID = nodes
                # Convert unicode to dictionary
                surveyAnswers = ast.literal_eval(entry["responses"])

                surveyData(i, questionID, surveyAnswers, dictSurveys)
    return dictSurveys
