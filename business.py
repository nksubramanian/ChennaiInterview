import hashlib
import uuid

from persistence_gateway import UnableToInsertDueToDuplicateKeyError, InvalidOperation


class UserInputError(Exception):
    pass


class Business:
    def __init__(self, template_repository, authorization, user_repository):
        self.persistence_gateway = template_repository
        self.authorization = authorization
        self.user_repository = user_repository

    def register(self, email, password, first_name, last_name):
        try:
            salt = uuid.uuid4().hex
            hashed_password = self.hash_password(password, salt)
            self.user_repository.create_user(first_name, last_name, email, hashed_password, salt)
        except UnableToInsertDueToDuplicateKeyError:
            raise UserInputError('ID already exist')

    @staticmethod
    def hash_password(password, salt):
        x = password + salt
        hashed_password = hashlib.sha512(x.encode('utf-8')).hexdigest()
        return hashed_password

    def login(self, email, password):
        user = self.user_repository.get_user(email)
        salt = user["salt"]
        hashed_password_db = user["password_hash"]
        hashed_password = self.hash_password(password, salt)
        if hashed_password_db == hashed_password:
            return self.authorization.get_token(email)
        else:
            raise UserInputError('Wrong Credentials')  #should this entire func be put in try


    def get_all(self, token):
        email = self.authorization.get_email(token)
        temp = self.persistence_gateway.get_all(email)
        return temp

    def insert(self, token, template_name, subject, body):
        email = self.authorization.get_email(token)
        x = self.persistence_gateway.insert(email, template_name, subject, body)
        return x

    def get(self, template_id, token):
        email = self.authorization.get_email(token)
        x = self.persistence_gateway.get(template_id, email)
        return x

    def update(self, token, template_name, subject, body, template_id):
        email = self.authorization.get_email(token)
        self.persistence_gateway.update(template_name, subject, body, email, template_id)

    def delete(self, token, template_id):
        email = self.authorization.get_email(token)
        self.persistence_gateway.delete(email, template_id)
