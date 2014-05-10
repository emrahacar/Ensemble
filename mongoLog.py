from pymongo import MongoClient

client = MongoClient('192.168.1.6',27017)
tah = client.mydb.tahminler
siralama = client.tjk.siralama


# Evaluator 
# dummy one
won1, won2, won3, lost1, lost2, lost3 = {}, {}, {}, {}, {}, {}
for x in tah.find({'kosId':80000}):
   metod = x['metod']
   won1[ metod ], won2[ metod ], won3[ metod ] = 0, 0, 0
   lost1[ metod ], lost2[ metod ], lost3[ metod ] = 0, 0, 0

kosId = 0

for tabela in siralama.find( {'kosId': {'$lt':80140}}):
   for x in tah.find({'kosId': tabela['kosId']}):
      s = tabela['sira']
      xlist = ['kosId', 'day', 'month', 'year', 'sehir', 'metod']
      try: 
         tahminler = [int(x[i]) for i in 'abcd']
      except:
         try: 
            tahminler = [int(x[i]) for i in 'abc']
         except:
            tahminler = [int(x[i]) for i in 'ab']
      
      try:
         gelen = [int(s[i]) for i in '123']
      except:
         gelen = [int(s[i]) for i in '12']
         
      metod = x['metod']
      if x['kosId']!=kosId:
         kosId = x['kosId']
         print [x[i] for i in xlist]

      if gelen[0] in tahminler[:1]: 
         won1[ metod ] += 1
      else:
         lost1[ metod ] += 1
      if gelen[0] in tahminler[:2]: 
         won2[ metod ] += 1
      else:
         lost2[ metod ] += 1
      if gelen[0] in tahminler[:3]: 
         won3[ metod ] += 1
      else:
         lost3[ metod ] += 1
      
      debugThis = 0
      if debugThis:
         print 'kosId', [x[i] for i in xlist]
         print 'Ilk 3', gelen
         print 'KosId', 
         if gelen[0] in tahminler: print '----------------------------> TUTTU '
         print ""

