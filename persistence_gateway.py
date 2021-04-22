import pymongo
from bson import ObjectId


class PersistenceGateway:
    def __init__(self, templates_db):
        self.templates_db = templates_db

    def add(self, mydict):
        x = self.templates_db['collection'].insert_one(mydict).inserted_id
        return str(x)

    def get(self, template_id, email):
        x = self.templates_db['collection'].find_one({'_id': ObjectId(template_id), 'email': email})
        x['template_id'] = str(x.pop('_id'))
        return x




    def get_all(self, email):
        x = self.templates_db['collection'].find_one({'email': email})
        x['template_id'] = x.pop('_id')
        x['template_id'] = template_id
        if x['email'] == email:
            return x


