import pymongo

mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = mongo_client.CompKeyExp
