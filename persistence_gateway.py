import pymongo


class PersistenceGateway:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]

    def add(self, collection, mydict):
        x = self.mydb[collection].insert_one(mydict)
        print("I am here")

    def get(self, collection, identity):
        x = self.mydb[collection].find_one({'_id': identity})
        x['id'] = x.pop('_id')
        return x
