from bson import ObjectId


class TemplateRepository:
    def __init__(self, templates_db):
        self.templates_db = templates_db

    def insert(self, email, template_name, subject, body):
        payload = {'template_name': template_name, 'subject': subject, 'body': body, 'email': email}
        x = self.__get_collection().insert_one(payload).inserted_id
        return str(x)

    def update(self, template_name, subject, body, email, template_id):
        query = self.__create_query(email, template_id)
        payload = {'template_name': template_name, 'subject': subject, 'body': body, 'email': email}
        result = self.__get_collection().replace_one(query, payload)
        if result.matched_count == 0:
            raise InvalidOperation()

    def get(self, template_id, email):
        doc = self.__get_collection().find_one(self.__create_query(email, template_id))
        if doc is None:
            raise InvalidOperation()
        return self.__transform_doc(doc)

    def get_all(self, email):
        docs = self.__get_collection().find({"email": email})
        return list(map(self.__transform_doc, docs))

    @staticmethod
    def __transform_doc(doc):
        doc['template_id'] = str(doc.pop('_id'))
        del doc['email']
        return doc

    def delete(self, email,  template_id):
        query = self.__create_query(email, template_id)
        result = self.__get_collection().delete_one(query)
        if result.deleted_count == 0:
            raise InvalidOperation("Item is not found")

    def __get_collection(self):
        return self.templates_db['collection']

    @staticmethod
    def __create_query(email, template_id):
        return {"_id": ObjectId(template_id), "email": email}


class InvalidOperation(Exception):
    pass
