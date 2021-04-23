from bson import ObjectId
from pymongo.errors import DuplicateKeyError


class UnableToInsertDueToDuplicateKeyError(Exception):
    pass


class InvalidOperation(Exception):
    pass


class UserRepository:
    def __init__(self, templates_db):
        self.templates_db = templates_db

    def create_user(self, first_name, last_name, email, password_hash, salt):
        try:
            obj = {"_id": email,
                   "first_name": first_name,
                   "last_name": last_name,
                   "password_hash": password_hash,
                   "salt": salt}
            self.__get_user_collection().insert_one(obj)
        except DuplicateKeyError:
            raise UnableToInsertDueToDuplicateKeyError("User already exists")

    def __get_user_collection(self):
        return self.templates_db['users']

    def get_user(self, email):
        user = self.__get_user_collection().find_one({"_id": email})
        if user is None:
            raise InvalidOperation("Wrong Credentials")
        return user


class TemplateRepository:
    def __init__(self, templates_db):
        self.templates_db = templates_db

    def insert(self, email, template_name, subject, body):
        payload = {'template_name': template_name, 'subject': subject, 'body': body, 'email': email}
        x = self.__get_collection().insert_one(payload).inserted_id
        if x is None: #is it necessary
            raise InvalidOperation("Operation failed")
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
        if docs is None:
            raise InvalidOperation()
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
