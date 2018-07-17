#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import psycopg2
import numpy as np
import os
import json
import time
import datetime



def main():

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

 
if __name__ == "__main__":
    data = main()
    myJSON = data[0][0]
    counter = 1
    for item in myJSON:
        if item["trial_type"] == "AJDnews":
            print "Question: {}".format(counter)
            print "Premier News: "
            print [toDate(timeStamp) for timeStamp in item["premierNews"]]
            print 
            print "Alpha News: "
            print [toDateitem["alphaNews"]
            print
            print "First News: "
            print item["firstNews"]
            print
            counter += 1
        # if item["trial_type"] == "AJDquestion":
        #     if (item["trial_index"] - 1) % 4 == 0:
        #         print "BEFORE: "
        #         print item["statementResponse"]
        #     else:
        #         print "AFTER: "
        #         print item["statementResponse"]
        # print item