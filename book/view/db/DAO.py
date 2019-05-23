import pymongo

class MongoDB():
	def __init__(self):
		self.mongoURL = 'mongodb+srv://easy:easy0319@mongodb-owlwh.mongodb.net/test?retryWrites=true'
		self.client = pymongo.MongoClient(mongoURL)
		self.db = pymongo.database.Database(client, 'mongoDB')
	
class books():
	def __init__(self, db):
		

books = pymongo.collection.Collection(db, 'Books')
users = pymongo.collection.Collection(db, 'Users')
