from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import pickle

client = MongoClient('192.168.1.6',27017)
tah = client.mydb.tahminler
tah.create_index([("kosId", ASCENDING)])
X=[]
for x in tah.find( {'kosId' : {'$gt':0} }).sort('kosId'):
    X.append(x)
f= open('tahminler.pkl','wb')
pickle.dump(X,f)
f.close()

    
