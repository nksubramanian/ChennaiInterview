import pymongo
from bson import ObjectId
import copy


class PersistenceGateway:
    def __init__(self, templates_db):
        self.templates_db = templates_db

    def add(self, mydict):
        x = self.__get_collection().insert_one(mydict).inserted_id
        return str(x)

    def get(self, template_id, email):
        x = self.__get_collection().find_one(self.__create_query(email, template_id))
        x['template_id'] = str(x.pop('_id'))
        del x['email']
        return x

    def get_all(self, email):
        results = []
        for doc in self.__get_collection().find({"email": email}):
            doc['template_id'] = str(doc.pop('_id'))
            del doc['email']
            results.append(doc)
        return results

    def update(self, payload, template_id):
        email = payload["email"]
        query = self.__create_query(email, template_id)
        result = self.__get_collection().replace_one(query, payload)
        if result.matched_count == 0:
            raise InvalidOperation()

    def delete(self, email,  template_id):
        query = self.__create_query(email, template_id)
        result = self.__get_collection().delete_one(query)
        if result.deleted_count == 0:
            raise InvalidOperation("This operation is not permitted")

    def __get_collection(self):
        return self.templates_db['collection']

    def __create_query(self, email, template_id):
        return {"_id": ObjectId(template_id), "email": email}


class InvalidOperation(Exception):
    pass

