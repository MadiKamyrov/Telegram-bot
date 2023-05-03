import pymongo

client = pymongo.MongoClient('mongodb+srv://madiayzhalby:kanada19@cluster0.zodb7u9.mongodb.net/test')

db = client['students_db']
students_collection = db['students']





