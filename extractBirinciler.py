#!python - obselete
# done by doReadKosular.R

# obselete now
error:

from pymongo import MongoClient
import os
import re

client = MongoClient('192.168.1.6',27017)
birinciler = client.mydb.birinciler

# This script will prepare the record for each birinci from 
# y:/birinciler.txt

fname = 'Y:/birinciler.txt'
f = open(fname)
lines = f.readlines()
f.close()

for line in lines:
    if line[0]<'0' or line[0]>'9': continue
    l = line.split(',')
    try:
	b = {   'kosId' : int(l[0]),
		'cins'  : l[2],
		'pist'  : l[3],
		'bir' : int(l[7]) }
	# print b
        birinciler.insert(b)
    except:
	print 'Problem in ', line
	
       


	   



