#!python

incomplete

from pymongo import MongoClient
import os
import re

client = MongoClient('192.168.1.6',27017)
tahminler = client.mydb.tahminler

# This script will prepare the record for each log file
# place them into a mongodb server

harf = 'abcdefghijklmnopqrstuvwxyz'

def get_kosu(lines):
    k = 0
    kosu = {}
    base_kosu = {}
    kosular = []
    for line in lines:
	if 'Dim of XX' in line:
	    base_kosu['dimXX'] = int(re.sub('"', '', line.split()[-1]))
	if 'Dim of XXsubset' in line:
	    base_kosu['dimXXsubset'] = int(re.sub('"', '', line.split()[-1]))
	if 'Dim of TEST' in line:
	    base_kosu['dimTEST'] = int(re.sub('"', '', line.split()[-1]))

    for line in lines:
        l = line.split()
    	if '= kazanc = ' in line: 
	    kosu.update(base_kosu)
	    kosular.append(kosu)
            kosu = {}
            k = 0
        if '= gercek 1 =' in line: 
	    kosu = { 'metod': l[2], 'pist': l[4], 'cins' : l[5], 'kosId': int(l[7]), 'weight': float(l[13]) }
	if '[1]' in line: continue
	if len(l)>7 and k<4:
	    kosu[harf[k]] = int(l[1])
  	    k += 1
    return kosular

root_dir = '/mnt/2/runs/'
root_dir = 'Y:/'
dirs = [root_dir+i for i in ['FEB','MAR','APR','MAY','JUN']]
year = 2013
months={'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6}
sehirs={'sehir1':'ADANA', 
	'sehir2':'IZMIR',
	'sehir3':'ISTANBUL',
	'sehir4':'BURSA',
	'sehir5':'ANKARA',
	'sehir6':'URFA',
	'sehir7':'ELAZIG',
	'sehir8':'DIYARBAKIR',
	'sehir9':'KOCAELI'}
alldirs=[]
for dir in dirs:
   if not os.path.isdir(dir): continue
   subdirs = [i for i in os.listdir(dir) if len(i)<6]
   for subdir in subdirs:
       dirfiles = [i for i in os.listdir(dir + '/' + subdir) if 'log.' in i]
       month = months[ dir.upper() ]
       day = int(subdir[3:])
       sehir = sehirs[ dirfiles.split('.')[-1] ]
       for fname in dirfiles:
	  if fname[-1]=='~': continue
	  base_dict = { 'day': int(day), 'month' : int(month), 
			'year' : int(year),  'sehir': sehir }
          fp = open( dir + '/' + subdir + '/' + fname ) 
          lines = fp.readlines()
          fp.close()
          try: 
	      kosular = get_kosu( lines )
              for kosu in kosular:
 	          kosu.update(base_dict)
	          # tahminler.insert(kosu)	  
          except:
	      print 'Problem in', fname, dir


	   



