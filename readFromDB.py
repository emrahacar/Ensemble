from pymongo import MongoClient
client = MongoClient('192.168.1.6',27017)
tahminler = client.mydb.tahminler

basekosNo=78000
for i in range(100):
    kosNo = basekosNo + i
    print kosNo
    for k in tahminler.find({'kosId':kosNo}):
	print k