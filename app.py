import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["local"]

collist = mydb.list_collection_names()
if "provatrack" in collist:
  print("The collection exists.")

mycol = mydb["provatrack"]

for x in mycol.find():
  print(x)

