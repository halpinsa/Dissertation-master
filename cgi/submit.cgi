#!/usr/bin/python
import cgi
import cgitb
import sys
cgitb.enable()
import os
import psycopg2
import json
print "Content-Type: application/json"
print

f = open('req.txt' , 'r')
for line in f:
    p = line.strip()
f.close();

#Define our connection string
conn_string = "host='pgteach' dbname='online_questions' user='s1617355' password= %s sslmode='disable'" % p

# print the connection string we will use to connect
# print "Connecting to database\n	->%s" % (conn_string)

# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()

dataArray = []
# Data array stores JSON, randomCode
for line in sys.stdin:
	dataArray.append(line.strip())

data = dataArray[0]
randomCode = dataArray[1]

# f = open('data.json' , 'w')
# f.write(data);
# f.close();
# print "Connected!\n"

# Drop table
# cursor.execute("DROP TABLE test;")

# Create a table
# cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, randomCode varchar, data JSON);")

# Load some JSON

# Add some JSON
# cursor.execute("INSERT INTO test (data) VALUES '({})'".format(someData))

# insertString = "INSERT INTO test (randomCode, data) VALUES (%s, %s::json[])" % (randomCode, data)
# cursor.execute(insertString)

SQL = "INSERT INTO userData (randomCode, data) VALUES (%s, %s)"
insertValues = (randomCode, data)
cursor.execute(SQL, insertValues)

# Commit table
conn.commit()

# Close cursor
cursor.close()

# Close connection
conn.close()





print '''{
		"data": {
			"response": 200,
			"name": "Success"
		}
	}'''
print
