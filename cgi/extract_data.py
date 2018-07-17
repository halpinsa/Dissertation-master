__author__ = 's1005849'

import psycopg2

def retrieve_raw_entries():

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
    cursor.execute("SELECT data FROM userdata WHERE id > 35;")

    data = cursor.fetchall()

    # Commit table
    conn.commit()

    # Close cursor
    cursor.close()

    # Close connection
    conn.close()
    entries = [entry[0] for entry in data]
    return entries


def retrieve_game_choices():
    data = retrieve_raw_entries()
    game_choices = []
    for participantData in data:
        trials_found = False
        for entry in participantData:
            if entry["trial_type"] == "JMMcardgame":
                thrown_trials = len([t for t in entry["game_choices"] if len(t['cardsFlipped']) == 0])
                top_guessed = len([t for t in entry["game_choices"] if t['guessMade'] == 'T'])
                bottom_guessed = len([t for t in entry["game_choices"] if t['guessMade'] == 'B'])
                if thrown_trials > 10:
                    print "Coins: %s" % entry["coins"]
                    random_code = [e for e in participantData if e["trial_type"] == 'AJDrandom-code'][0]['randomCode']
                    print "More than 10 trials by participant thrown so results excluded. " \
                          "Number of trials thrown: %s. Turkers random code: %s" % (thrown_trials, random_code)
                    continue
                if top_guessed > 80:
                    print "Top guessed more than 90 times so excluded. " \
                          " Turkers random code: %s" % random_code
                    continue
                if bottom_guessed > 80:
                    print "Bottom guessed more than 90 times so excluded. " \
                          " Turkers random code: %s" % random_code
                    continue
                game_choices.append(entry["game_choices"])
                trials_found = True

        if not trials_found:
            game_choices.append(None)
    return game_choices

def all_game_choices():
    data = retrieve_raw_entries()
    game_choices = []
    for participantData in data:
        for entry in participantData:
            if entry["trial_type"] == "JMMcardgame":
                instructions_node = [e for e in participantData if e["trial_type"] == 'JMMinstructions'][0]
                thrown_trials = len([t for t in entry["game_choices"] if len(t['cardsFlipped']) == 0])
                if thrown_trials > 10:
                    random_code = [e for e in participantData if e["trial_type"] == 'AJDrandom-code'][0]['randomCode']
                    print "More than 10 trials by participant thrown so results excluded. " \
                          "Number of trials thrown: %s. Turkers random code: %s" % (thrown_trials, random_code)
                    print "Time Spent on Task: %s" % ((entry["time_elapsed"] - instructions_node["time_elapsed"])/60000)
                    continue

                game_choices.extend(entry["game_choices"])
    return game_choices
