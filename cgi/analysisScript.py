#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import psycopg2
import numpy as np
import datetime
import ast
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
import plotScript as ps
import rejectScript as rj
from scipy.stats import chisquare, f_oneway
import csv
import json
import os

# dictionary has keys 1...numQuestions, and holds arrays of prior and posterior
dict_prior_posterior = {}

# dictionary has keys 1...numQuestions, and holds arrays of responses as tuples
dict_clicks_on_news_buttons = {}

# dictionary has keys 18...21 and arrays of surveys
dict_surveys = {}

# dictionary has keys 1...numQuestions and values arrays of arrays of clicks
dict_for_against = {}


###############################
#  DICTIONARIES FOR users #
###############################

# dictionary has keys 0...numParticipants and values of first question response
dict_first_question = {}

# dictionary has keys 0...numParticipants and values of arrays of arrays of clicks
dict_user_browsing = {}

# dictionary has keys 0...numParticipants and values of arrays of tuples
dict_user_beliefs = {}

# dictionary 
dict_user_time = {}

# dictionary has keys 0...numParticipants and arrays of tuples of bias
dict_bias = {}

# dictionary has keys 0...numParticipants and values 
dict_user_clicks = {}

# dictionary has keys 0...numParticipants
dict_user_answers = {}

# dictionary has keys 0...numParticipants
dict_user_first_click = {}

###########################
#  DICTIONARIES FOR BONUS #
###########################

#dict has keys of coin score, and values of arrays of participantNum
dict_user_bonus = {}



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
    ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
    ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
    ['Not difficult at all', 'Somewhat difficult', 'Very difficult', 'Extremely difficult']
]

OPTIONS_LOTR = [
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"],
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"],
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"],
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"],
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"],
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"],
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"],
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"],
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"],
    ["I agree a lot", "I agree a little", "I neither agree nor disagree", "I disagree a little", "I disagree a lot"]
]

STATEMENTS = [
    "Brexit", "Conspiracy", "Trump", "World in 20yrs",
    "HS2", "NuclearWar", "Young People", "PC", "Hard-work", "AI"
]


def get_data(val):

    # If file exists then load it, and don't query DB
    if os.path.isfile(val+".txt"):
        with open(val+".txt") as data_file:    
            data = json.load(data_file)
        return data

    # Define our connection string
    conn_string = "host='pgteach' dbname='online_questions'"

    # print the connection string we will use to connect
    print "Connecting to database\n ->%s" % conn_string

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!\n"

    # conn.cursor
    cursor.execute("SELECT {} FROM accepted_users".format(val))

    data = cursor.fetchall()

    # Commit table
    conn.commit()

    # Close cursor
    cursor.close()

    # Close connection
    conn.close()

    # Save the data
    with open(val+'.txt', 'w') as f:
        json.dump(data, f)
	

    return data


def to_date(time_stamp):
    return datetime.datetime.fromtimestamp(
        int(time_stamp / 1e3)
    ).strftime('%Y-%m-%d %H:%M:%S')


def add_to_dict(dictionary, key, entry):
    if key not in dictionary:
        dictionary[key] = [entry]
    else:
        dictionary[key].append(entry)


def create_survey_score(question_id, survey_answers):
    count = 0
    for k, v in survey_answers.iteritems():
        # LOT-R
        if question_id == 18:
            q = int(k[1])
            if q in [1, 4, 5, 7]:
                pass
            else:
                idx = OPTIONS_LOTR[q].index(v)
                if q in [2, 6, 8]:
                    pass
                else:
                    # Reverse score
                    idx = 4 - idx
                count += idx

        # SPQ-B
        elif question_id == 19:
            if v == "Yes":
                count += 1
        # ALTMAN
        elif question_id == 20:
            idx = OPTIONS_ALTMAN[int(k[1])].index(v)
            count += idx
        # PHQ-9
        elif question_id == 21:
            if int(k[1]) == 9:
                pass
            else:
                idx = OPTIONS_PHQ[int(k[1])].index(v)
                count += idx

    add_to_dict(dict_surveys, question_id, count)


def user_stats():
    total_correct_questions = []
    total_correct_updates_by_strength = {"Strong": 0, "Moderate": 0, "Mild": 0}
    total_incorrect_updates_by_strength = {"Strong": 0, "Moderate": 0, "Mild": 0}
    for eachUser in range(NUM_PARTICIPANTS):
        num_correct_updates = 0
        correct_questions = []
        correct_updates_by_strength = {"Strong": 0, "Moderate": 0, "Mild": 0}
        incorrect_updates_by_strength = {"Strong": 0, "Moderate": 0, "Mild": 0}

        print "Participant: {}".format(eachUser)
        print "------------------"
        # print "LOT-R: {} / ".format(dictSurveys[18][eachUser])
        # print "SPQ-B: {}".format(dictSurveys[19][eachUser])
        # print "Altman: {}".format(dictSurveys[20][eachUser])
        # print "PHQ-9: {}".format(dictSurveys[21][eachUser])
        # print "-------------------"
        for eachQuestion in range(1, 11):
            prior = dict_prior_posterior[eachQuestion][eachUser][0]
            numFor, numAgainst = dict_for_against[eachQuestion][eachUser]
            posterior = dict_prior_posterior[eachQuestion][eachUser][1]

            # Strong
            if (1 <= prior < 16) or (82 <= prior <= 100):
                beliefState = "Strong"
            elif (16 <= prior < 33) or (66 <= prior < 82):
                beliefState = "Moderate"
            else:
                beliefState = "Mild"

            if prior >= 0:
                if (posterior >= prior and numFor > numAgainst) or \
                        (posterior < prior and numFor < numAgainst):
                    num_correct_updates += 1
                    correct_questions.append(STATEMENTS[eachQuestion - 1])
                    correct_updates_by_strength[beliefState] += 1
                else:
                    incorrect_updates_by_strength[beliefState] += 1
            else:
                if (posterior <= prior and numFor > numAgainst) or \
                        (posterior > prior and numFor < numAgainst):
                    num_correct_updates += 1
                    correct_questions.append(STATEMENTS[eachQuestion - 1])
                    correct_updates_by_strength[beliefState] += 1
                else:
                    incorrect_updates_by_strength[beliefState] += 1

        total_correct_questions.extend(correct_questions)
        for k, v in correct_updates_by_strength.iteritems():
            total_correct_updates_by_strength[k] += v
            total_incorrect_updates_by_strength[k] += incorrect_updates_by_strength[k]
            total = v + incorrect_updates_by_strength[k]
            print "{0}: {1}/{2}".format(k, v, total)
        print

    dictCorrectQuestionCounts = {i: total_correct_questions.count(i) for i in total_correct_questions}

    print "Dict of correct question counts:"
    print dictCorrectQuestionCounts
    for k, v in total_correct_updates_by_strength.iteritems():
        total = v + total_incorrect_updates_by_strength[k]
        print "{0}: {1}/{2} ({3})".format(k, v, total, (float(v) / total))


def addNews(questionID, lenAlpha, lenPremier, lenFirst):
    newsTuple = (
        lenAlpha,
        lenPremier,
        lenFirst
    )

    if questionID not in dict_clicks_on_news_buttons:
        dict_clicks_on_news_buttons[questionID] = [newsTuple]
    else:
        dict_clicks_on_news_buttons[questionID].append(newsTuple)


def addForAgainst(questionID, numFor, numAgainst, numAlpha, numPremier):
    forAgainstTuple = (
        numFor + numAlpha,
        numAgainst + numPremier
    )

    if questionID not in dict_for_against:
        dict_for_against[questionID] = [forAgainstTuple]
    else:
        dict_for_against[questionID].append(forAgainstTuple)


def getTotalNewsClicks(include_conspiracy=True):
    # Participant News Clicks
    # List which stores each participants total clicks
    participantTotalNewsClicks = np.zeros((NUM_PARTICIPANTS, 3))

    # Question responses
    # List which stores lists of the total clicks per question
    questionTotalNewsClicks = []

    for i in range(1, 11):
        if i == 2 and not include_conspiracy:
            pass
        else:
            questionTotalNewsClicks.append(np.sum(np.asarray([np.asarray(x) for x in dict_clicks_on_news_buttons[i]]), axis=0))
            participantTotalNewsClicks += np.asarray([np.asarray(x) for x in dict_clicks_on_news_buttons[i]])

    # Convert array to numpy array
    questionTotalNewsClicks = np.asarray(questionTotalNewsClicks)

    totalNewsClicks = np.sum(participantTotalNewsClicks, axis=0)

    return totalNewsClicks, questionTotalNewsClicks, participantTotalNewsClicks


def makeGraphs():
    totalNewsClicks, questionTotalNewsClicks, participantTotalNewsClicks = getTotalNewsClicks()
    chisq_p_values_1, chisq_p_values_2 = chi_square_users()

    idxs = [0, 1, 2]
    channels = ["Alpha", "Premier", "First"]

    figureID = 1

    # ps.plotTotalClicks(figureID, idxs, totalNewsClicks, channels)
    # figureID += 1
    
    # ps.plotMeanClicks(figureID, idxs, participantTotalNewsClicks, NUM_PARTICIPANTS, channels)
    # figureID += 1

    # ps.plotClicksPerAnswer(figureID, idxs, questionTotalNewsClicks, channels)
    # figureID += 1

    # ps.plotMeanClicksPerAnswer(figureID, idxs, NUM_PARTICIPANTS, dict_clicks_on_news_buttons, channels)
    # figureID += 1

    # ps.plotPriorAndPosteriorBar(figureID, NUM_PARTICIPANTS, dict_prior_posterior)
    # figureID += 11

    # # ps.plotIndividualClicks(figureID, idxs, participantTotalNewsClicks, channels, NUM_PARTICIPANTS)
    # # figureID += 1

    # ps.plotBias(figureID, NUM_PARTICIPANTS, dict_bias)
    # figureID += 1

    # ps.plotPriorAlpha(figureID, dict_prior_posterior, dict_clicks_on_news_buttons)
    # figureID += 1

    # ps.plotPriorPremier(figureID, dict_prior_posterior, dict_clicks_on_news_buttons)
    # figureID += 1

    # ps.plotPriorFirst(figureID, dict_prior_posterior, dict_clicks_on_news_buttons)
    # figureID += 1

    # ps.plotMeanBias(figureID, idxs, channels, dict_bias, NUM_PARTICIPANTS)
    # figureID += 1

    # ps.plotLOTROptimism(figureID, NUM_PARTICIPANTS, dict_surveys, dict_prior_posterior)
    # figureID += 1

    # ps.plotSPQBParanoia(figureID, NUM_PARTICIPANTS, dict_surveys, dict_prior_posterior)
    # figureID += 1

    # ps.plotManiaUpdate(figureID, NUM_PARTICIPANTS, dict_surveys, dict_prior_posterior)
    # figureID += 1

    # ps.plotSPQUpdate(figureID, NUM_PARTICIPANTS, dict_surveys, dict_prior_posterior)
    # figureID += 1

    # ps.plotMeanClicksAlpha(figureID, NUM_PARTICIPANTS, dict_user_clicks, dict_user_beliefs,
    #     dict_clicks_on_news_buttons)
    # figureID += 1

    # ps.plotPValsBrowsing(chisq_p_values_1, chisq_p_values_2)
    # figureID += 1

    # ps.plotAlphaClicksPerQuestion(figureID, NUM_PARTICIPANTS, dict_clicks_on_news_buttons)
    # figureID += 1

    ps.plotHeatmapPriorPosterior(figureID, NUM_PARTICIPANTS, dict_prior_posterior)
    figureID += 1


    plt.show()


def millisecondsToSeconds(time_elapsed):
    millis = time_elapsed
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24

    return ("%d:%d:%d" % (hours, minutes, seconds))


def addUserCoinScore(cardgameData, participantNum):
    end_coins = 0
    for trial in cardgameData:
        if 'coins' in trial:
            end_coins = trial['coins']

    add_to_dict(dict_user_bonus, end_coins, participantNum)


def print_user_coin_score():
    count = 0
    for k in sorted(dict_user_bonus.iterkeys()):
        if count > 57:
            print "1$ BONUS"
        if len(dict_user_bonus[k]) > 1:
            for id in dict_user_bonus[k]:
                print "{0}: ID: {1}, code: {2}".format(k, id, randomCodeVals[id])
                count += 1
        else:
            print "{0}: ID: {1}, code: {2}".format(k, dict_user_bonus[k][0], randomCodeVals[dict_user_bonus[k][0]])
            count += 1


def addDataToDicts(data):
    num_clicks_alpha = 0
    num_clicks_first = 0
    num_clicks_premier = 0
    for participantNum, participantData in enumerate(data):
        user_first_click_list = []
        for entry in participantData:
            # print entry["trial_type"]
            time_elapsed = entry["time_elapsed"]

            # Get the node ID
            nodes = [int(float(val)) for val in entry["internal_node_id"].split("-")]

            # print "Node id: {}, Block name: {}".format(
            #     entry["internal_node_id"], entry["trial_type"])

            # Get the bias rating for participant
            if len(nodes) != 3 and entry["trial_type"] == "AJDbias-rating":
                tupleBias = (
                    entry["alphaBias"], entry["premierBias"], entry["firstBias"]
                )

                dict_bias[participantNum] = tupleBias

            # Get the survey results for each participant
            elif len(nodes) != 3 and entry["trial_type"] == "AJDsurvey":
                _, questionID = nodes

                # Convert unicode to dictionary
                surveyAnswers = ast.literal_eval(entry["responses"])

                create_survey_score(questionID, surveyAnswers)

            # Get coin totals
            elif entry["trial_type"] == "JMMcardgame":
                addUserCoinScore(entry["game_choices"], participantNum)
                

            # Ignore instruction blocks etc.
            elif len(nodes) != 3:
                pass

            # Skip first question of participants
            # becuase we added an extra block of instructions
            # Add the first question response
            elif nodes[1] == 1:
                if nodes[2] == 0:
                    add_to_dict(dict_first_question, participantNum, entry["statementResponse"])



            # Process statement and news blocks
            else:
                _, questionID, blockID = nodes

                # Correct for first block
                # Question IDs are from 1...11
                questionID -= 1

                # Prior 
                if blockID == 0:
                    prior = entry["statementResponse"] - 50.0

                # Posterior
                if blockID == 2:
                    posterior = entry["statementResponse"] - 50.0

                    add_to_dict(dict_prior_posterior, questionID, (prior, posterior))

                    add_to_dict(dict_user_beliefs, participantNum, (prior, posterior))

                # News
                if blockID == 1:
                    # Alpha in favour
                    # Premier against
                    # First neutral
                    addNews(
                        questionID,
                        len(entry["alphaNews"]),
                        len(entry["premierNews"]),
                        len(entry["firstNews"])
                    )

                    addForAgainst(
                        questionID,
                        entry["firstForAgainst"].count("for"),
                        entry["firstForAgainst"].count("against"),
                        len(entry["alphaNews"]),
                        len(entry["premierNews"])
                    )

                    if participantNum not in dict_user_clicks:
                        dict_user_clicks[participantNum] = np.array(
                            [len(entry["alphaNews"]),
                            len(entry["premierNews"]),
                            len(entry["firstNews"])]
                        )
                    else:
                        # print "here"
                        dict_user_clicks[participantNum] = np.add(np.array(
                            [len(entry["alphaNews"]),
                            len(entry["premierNews"]),
                            len(entry["firstNews"])]
                        ), dict_user_clicks[participantNum])

                    # Add news click timestamps to dict
                    list_of_news_clicks = []
                    list_of_news_clicks.extend(
                        entry["alphaNews"] + 
                        entry["premierNews"] + 
                        entry["firstNews"]
                    )
                    list_of_news_clicks.sort()

                    add_to_dict(dict_user_browsing, participantNum, list_of_news_clicks)

                    # Get time of first click
                    question_first_click = 0
                    first_click_time = list_of_news_clicks[0]
                    if first_click_time in entry["alphaNews"]:
                        num_clicks_alpha += 1
                    elif first_click_time in entry["premierNews"]:
                        num_clicks_premier += 1
                        question_first_click = 1
                    else:
                        num_clicks_first += 1
                        question_first_click = 2

                    user_first_click_list.append(question_first_click)

        dict_user_first_click[participantNum] = user_first_click_list       

        time_elapsed = millisecondsToSeconds(time_elapsed)
        add_to_dict(dict_user_time, participantNum, time_elapsed)
    first_clicks(num_clicks_alpha, num_clicks_premier, num_clicks_first)


def checkRejection():
    for user in range(NUM_PARTICIPANTS):
        sliderVal = dict_first_question[user][0]
        userUpdate = dict_user_beliefs[user]
        browsing = dict_user_browsing[user]

        userPassed = [1, 1, 1]
        print "Testing user: {}".format(user)
        print "{}".format(randomCodeVals[user])
        # Check they answered q1 correctly
        if not rj.passedFirstQuestion(sliderVal):
            userPassed[0] = 0
        if not rj.passedExtremeUpdate(userUpdate):
            userPassed[1] = 0
        if not rj.passedNewsBrowsing(browsing):
            userPassed[2] = 0

        if all(i == 1 for i in userPassed):
            print "OK!"
        else:
            if userPassed[0] != 1:
                print "Q1: FAILED"
            if userPassed[1] != 1:
                print "Update: FAILED"
            if userPassed[2] != 1:
                print "Browsing: FAILED"
        print dict_user_time[user]
        print "------------------"
        print


def show_survey_results():
    # LOT-R - 18
    list_of_surveys = ["LOT-R", "SPQ-B", "ALTMAN", "PHQ-9"]
    for idx, survey_id in enumerate([18, 19, 20, 21]):
        print list_of_surveys[idx]
        print "-------------------"
        survey_results = dict_surveys[survey_id]
        # print survey_results
        print "Mean: {}".format(np.mean(survey_results))
        print "Std. Dev: {}".format(np.std(survey_results))
        print


def print_chisq_main_news():
    totalNewsClicks, questionTotalNewsClicks, participantTotalNewsClicks = getTotalNewsClicks()
    chisq, p = chisquare(totalNewsClicks)
    print "Probability total news clicks is equally distributed: {}".format(p)

    listOfParticipantsWithBrowsingDifferences = []
    for i, participant in enumerate(participantTotalNewsClicks):
        chisq, p = chisquare(participant)
        if p <= 0.05:
            listOfParticipantsWithBrowsingDifferences.append(i)
    print listOfParticipantsWithBrowsingDifferences

    totalNewsClicks, questionTotalNewsClicks, participantTotalNewsClicks = getTotalNewsClicks(include_conspiracy=False)
    listOfParticipantsWithBrowsingDifferences = []
    for i, participant in enumerate(participantTotalNewsClicks):
        chisq, p = chisquare(participant)
        if p <= 0.05:
            listOfParticipantsWithBrowsingDifferences.append(i)
    print listOfParticipantsWithBrowsingDifferences


def first_clicks(alpha, premier, first):
    total = float(alpha + premier + first)
    print total
    print "Distribution of initial clicks"
    print "----------------------------"
    print "Alpha: {:.2f}%".format((alpha / total)*100)
    print "Premier: {:.2f}%".format((premier / total)*100)
    print "First: {:.2f}%".format((first / total)*100)
    print


def ANOVA_mean_clicks():
    _, _, user_clicks = getTotalNewsClicks()
    F, p = f_oneway(
        user_clicks[:, 0],
        user_clicks[:, 1],
        user_clicks[:, 2],
    )

    print F, p
    print np.var(user_clicks, axis=0)


def ANOVA_mean_clicks_each_question():
    for question_id in range(1, 11):
        click_values = np.zeros((NUM_PARTICIPANTS, 3))
        for idx, each_user in enumerate(dict_clicks_on_news_buttons[question_id]):
            click_values[idx] = each_user

        F, p = f_oneway(
            click_values[:, 0],
            click_values[:, 1],
            click_values[:, 2]
        )

        print "Question: {}, F: {:.2f}, p: {:.2f}".format(STATEMENTS[question_id-1],F, p)


def chi_square_users():
    chisq_p_values_1 = []
    chisq_p_values_2 = []
    # anova_p_values = []
    total_conf_bias = 0
    for user in range(NUM_PARTICIPANTS):
        vals = np.zeros((10, 3))
        for question_id in range(1, 11):
            if question_id == 2:
                continue
            vals[question_id-1] = dict_clicks_on_news_buttons[question_id][user]


        F, p_ANOVA = f_oneway(vals[:, 0], vals[:, 1], vals[:, 2])
        chisq, p_chisq = chisquare(np.sum(vals, axis=0))
        if p_chisq <= 0.05:
            if np.argmax(np.sum(vals, axis=0)) == 0:
                total_conf_bias += 1

            # print np.sum(vals, axis = 0)

        chisq_p_values_1.append(p_chisq)
        # anova_p_values.append(p_ANOVA)

    for user in range(NUM_PARTICIPANTS):
        vals = np.zeros((10, 3))
        for question_id in range(1, 11):
            vals[question_id-1] = dict_clicks_on_news_buttons[question_id][user]


        chisq, p_chisq = chisquare(np.sum(vals, axis=0))
        chisq_p_values_2.append(p_chisq)
    # print total_conf_bias
    return chisq_p_values_1, chisq_p_values_2



if __name__ == "__main__":
    data = get_data("data")  # returns (data,)
    data = [entry[0] for entry in data]


    NUM_PARTICIPANTS = len(data)

    randomCodeVals = get_data("randomcode")
    addDataToDicts(data)

    # user_stats()
    makeGraphs()
    # print_user_coin_score()
    # checkRejection()
    # print_chisq_main_news()
    # show_survey_results()
    # print dict_user_clicks
    # print dict_clicks_on_news_buttons[1]
    # ANOVA_mean_clicks()
    # ANOVA_mean_clicks_each_question()
    # chi_square_users()
    # print dict_clicks_on_news_buttons

    # _, _, clicks = getTotalNewsClicks()
    # a = np.argmax(clicks, axis=1)
    # print np.count_nonzero(a == 0)
    # print np.count_nonzero(a == 1)
    # print np.count_nonzero(a == 2)
    # print dict_user_first_click
    # user_first_clicks = np.zeros((NUM_PARTICIPANTS, 10))
    # for k in range(NUM_PARTICIPANTS):
    #     user_first_clicks[k] = dict_user_first_click[k]

    # user_first_clicks = user_first_clicks.astype(int)

    # for i in range(10):
    #     print np.bincount(user_first_clicks[:,i])




        
