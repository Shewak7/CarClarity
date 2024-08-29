import pymongo 

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myClient["Car"]
Collection = db["carStat"]