import pymongo


class PersistenceGateway:
    def __init__(self, mydb):
        self.mydb = mydb


    def add(self, collection, mydict):
        x = self.mydb[collection].insert_one(mydict)

    def get(self, collection, identity):
        x = self.mydb[collection].find_one({'_id': identity})
        x['id'] = x.pop('_id')
        return x
