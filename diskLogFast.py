import pickle
import json
import numpy as np

debugThis = 0
won1, won2, won3, won4, lost1 = {}, {}, {}, {}, {}
weights, multweights = {}, {}
Tahminler = {}
X = []
Siralama = {}
metods=set()

def tahminDerecelendir(gelen, metod, tahminler):
   global won1, won2, won3, won4, lost1
   if gelen[0] in tahminler[:1]: 
      won1[ metod ] += 1
   else:
      lost1[ metod ] += 1
   if gelen[0] in tahminler[:2]: 
      won2[ metod ] += 1
   if gelen[0] in tahminler[:3]: 
      won3[ metod ] += 1
   if gelen[0] in tahminler[:4]: 
      won4[ metod ] += 1
      
def debugThisKosu(kosId, keys, tahminS, weights, s):
   global debugThis
   if debugThis<2: return
   print 'kosId', kosId
   for key in keys:
      print key, 100.0 * tahminS[key] / weights[AGG]
   print 'Siralama', s

def initTahminSiralama():
   global metods, Tahminler, X, Siralama
   # this is not working
   print 'initTahminSiralama for the first time'
   if None:
      try: 
         f = open('kosu/tahminler.pkl')
      except:
         f = open('c:/Emrah/TJK/R/kosu/tahminler.pkl','rb')
      X = pickle.load(f)
      f.close()
 
   metods=set()
   Tahminler = {}
   X = []
   f = open('kosu/tahminler.txt')
   for line in f:
      l = line.strip()
      # poor man's solution
      l = l.replace("u'","'").replace("'",'"')
      l = l.replace('ObjectId','')
      l = l.replace('(','')
      l = l.replace(')','')
      x = json.loads(l)
      X.append(x)
      try:
         Tahminler[ x['kosId'] ].append( x )
      except:
         Tahminler[ x['kosId'] ] = [ x ]
      metods.add( x['metod'] )
   f.close()

   # read siralama from the text file. faster ?
   Siralama={}
   try:
      f = open('kosu/siralamalar.txt','rb')
   except:
      f = open('C:/Emrah/TJK/R/kosu/siralamalar.txt','rb')
   for line in f:
      d=json.loads(line.strip())
      Siralama[ d['kosId'] ] = d['sira']
   f.close()
   return



def doExperiment(query, extramultweights = {}, odul = [1.75, 1.25, 1.01], kosCins='ARA'):
   global won1, won2, won3, won4, lost1

   if len(X) == 0: initTahminSiralama()
   # initialize
   AGG=u'AGG'
   kosIds = set()
   metods.add(AGG)
   for metod in metods:
      won1[ metod ], won2[ metod ], won3[ metod ] = 0, 0, 0
      won4[ metod ], lost1[ metod ] = 0, 0
      weights[ metod ] = []
      multweights[ metod ] = 1.0
      
   # always override the top extramultweights
   multweights.update( extramultweights )
   totcount = 0.0
   tahminS = {}
   kosId = 0
   # go over all guesses made.
   querykeys = list(query)
   for x in [x for x in X if x['cins'] == kosCins]:
      if not int(x['kosId']) in Siralama: 
         if debugThis>3: print 'Siralama not ready for', int(x['kosId'])
         continue
         
      if not x['kosId'] == kosId:
         # Finalize x['kosId']
         # to it after the loop too
         if len(tahminS):
            keys = sorted(tahminS, key=lambda x: -tahminS[x])
            tahminDerecelendir(s, AGG, keys)
            debugThisKosu(kosId, keys, tahminS, weights, s)
         
         # prepare for next one
         weights[AGG] = 0.0
         tahminS = {}
         kosIds.add( kosId )
         kosId = x['kosId']
      
      # xlist = ['kosId', 'day', 'month', 'year', 'sehir', 'metod']
      tahminler = [int(x[i]) for i in 'abcd' if i in x] 
      s = Siralama[ int(x['kosId']) ]
      try:
         gelen = s[:3]
      except:
         gelen = s[:2]
      metod = x['metod']

      # tahmin derecelendir l* metods
      tahminDerecelendir(gelen, metod, tahminler)
      
      # ensemble hazirligi
      weights[ metod ].append( x['weight'] )
      for i in tahminler:
         if not i in tahminS: tahminS[ i ] = 0.0

      weights[AGG] += float(x['weight'])
      # AGG odullerini dagitalim. 
      for i, o in enumerate(odul):
         # S = 1,2,3,4.. odul aliyor, 
         # x['weight'] assigned by the code
         # o: odul miktari
         # multweights[ metod ] top overrides.
         if len(tahminler)>(i+1): tahminS[ tahminler[i] ] += x['weight'] * o * multweights[ metod ]

   #   
   # son kosuicin tahmin AGG alalim
   if len(tahminS):
      keys = sorted(tahminS, key=lambda x: -tahminS[x])
      tahminDerecelendir(s, AGG, keys)
      debugThisKosu(kosId, keys, tahminS, weights, s)
     
   # The below will put a list of Winning Rations using 1st, 2nd, 3rd and 4th guesses.
   # 
   if debugThis:
      print 'Report for q' + str(query)
      print won1['l']+lost1['l'], ' Tahmin ', 
      print len(kosIds), ' Kosu Icinden'
      keys =  sorted(won1, key=lambda x: won1[x]/float(won1[x]+lost1[x]))
      for key in keys:
         tot = float(won1[key]+lost1[key])/100.0
         print '{:<20} {:f} {:f} {:f} {:f} \t {:f} '.format(key, won1[key]/tot, won2[key]/tot, won3[key]/tot, won4[key]/tot, np.mean(weights[key]))

   key = AGG
   tot = float(won1[key]+lost1[key])/100.0
   return ( won1[key]/tot, won2[key]/tot, won3[key]/tot, won4[key]/tot )

            

