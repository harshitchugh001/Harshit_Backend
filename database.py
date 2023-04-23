import pymongo


client = pymongo.MongoClient("mongodb+srv://harsh:3125@cluster0.uzpmmuw.mongodb.net/?retryWrites=true&w=majority")
# database
db = client.data
# collection
collection = db.test