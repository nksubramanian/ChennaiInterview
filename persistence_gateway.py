import pymongo
from bson import ObjectId
import copy


class PersistenceGateway:
    def __init__(self, templates_db):
        self.templates_db = templates_db

    def add(self, mydict):
        x = self.templates_db['collection'].insert_one(mydict).inserted_id
        return str(x)

    def get(self, template_id, email):
        x = self.templates_db['collection'].find_one({'_id': ObjectId(template_id), 'email': email})
        x['template_id'] = str(x.pop('_id'))
        del x['email']
        return x

    def get_all(self, email):
        results = []
        for doc in self.templates_db['collection'].find({"email": email}):
            doc['template_id'] = str(doc.pop('_id'))
            del doc['email']
            results.append(doc)
        print(results)
        return results

    def update(self, payload, template_id):
        query = {"_id": ObjectId(template_id), "email": payload["email"]}
        result = self.templates_db['collection'].replace_one(query, payload)

    def delete(self, payload, template_id):
        pass


