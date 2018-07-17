#!/usr/bin/env python
import psycopg2
import numpy as np
import os
import json

def main():
    #Define our connection string
    conn_string = "host='pgteach' dbname='online_questions'"
 
    # print the connection string we will use to connect
    print "Connecting to database\n ->%s" % (conn_string)
 
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!\n"

    # Drop table
    # cursor.execute("DROP TABLE userData;")
    
    # Create a table
    # cursor.execute("CREATE TABLE userData (id serial PRIMARY KEY, data json, randomCode varchar);")

    # Load some JSON
    # with open("../cgi/data.json") as f:
    #     for line in f:
    #         print line.strip()
    #         someData = line.strip()

    # Add some JSON
    # cursor.execute("INSERT INTO test (data) VALUES '({})'".format(someData))
    # cursor.execute("INSERT INTO test (data, randomCode) VALUES ('{}', '{}')".format(someData, 'h637d8hA'))

    # Commit table
    # conn.commit()

    # Close cursor
    cursor.close()

    # Close connection
    conn.close()
 
if __name__ == "__main__":
    main()
