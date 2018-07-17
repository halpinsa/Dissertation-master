#!/usr/bin/python
import cgi
import cgitb
import sys
cgitb.enable()
print "Content-Type: text/json"
print
data = sys.stdin.read();
f = open('data.json' , 'w')
f.write(data);
f.close();
