#!python

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
dirs = [root_dir+i for i in os.listdir('Y:/') if '201' in i]

for dir in dirs:
   if not os.path.isdir(dir): continue
   try:
       tmp=int(dir[len(root_dir)])
   except:
       continue
   print 'Processing Directory', dir
   dirfiles = [i for i in os.listdir(dir) if '.log' in i]
   for fname in dirfiles:
      if fname[-1]=='~': continue
      day, month, year, sehir = dir.split('.')[:4]
      day=day[(len_root_dir):]
      sehir, kosuNo = fname.split('.')[:2]
      base_dict = { 'day': int(day), 'month' : int(month), 'year' : int(year), 
		    'sehir': sehir, 'kosuNo' : kosuNo }
      fp = open( dir + '/' + fname ) 
      lines = fp.readlines()
      fp.close()
      try: 
	  kosular = get_kosu( lines )
          for kosu in kosular:
 	      kosu.update(base_dict)
	      tahminler.insert(kosu)	  
      except:
	  print 'Problem in', fname, dir


	   



