import pymongo


class PersistenceGateway:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]

    def add(self, collection, mydict):
        x = self.mydb[collection].insert_one(mydict)
        print("I am here")

    def update(self, collection, id_, data_dictionary):
        pass
