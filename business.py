import hashlib
import uuid

from persistence_gateway import UnableToInsertDueToDuplicateKeyError, InvalidOperation
from authorization import AuthenticationError


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
        try:
            user = self.user_repository.get_user(email)
            salt = user["salt"]
            hashed_password_db = user["password_hash"]
            hashed_password = self.hash_password(password, salt)
            if hashed_password_db == hashed_password:
                return self.authorization.get_token(email)
            else:
                raise UserInputError('Wrong Credentials')
        except InvalidOperation:
            raise UserInputError('Wrong Credentials')

    def insert(self, token, template_name, subject, body):
        try:
            email = self.authorization.get_email(token)
            x = self.persistence_gateway.insert(email, template_name, subject, body)
            return x
        except InvalidOperation: #is it necssary, can create fake tokens and insert
            raise UserInputError('Wrong Credentials')
        except AuthenticationError:
            raise UserInputError('Authentication failed')
        except Exception:
            raise UserInputError('Miscellaneous')



    def get(self, template_id, token):
        try:
            email = self.authorization.get_email(token)
            x = self.persistence_gateway.get(template_id, email)
            return x
        except InvalidOperation:
            raise UserInputError('Operation not allowed')
        except AuthenticationError:
            raise UserInputError('Authentication failed')
        except Exception: #not necessary
            raise UserInputError('Wrong Credentials invalid token')

    def get_all(self, token):
        try:
            email = self.authorization.get_email(token)
            temp = self.persistence_gateway.get_all(email)
            return temp
        except InvalidOperation:
            raise UserInputError('Operation not allowed')
        except AuthenticationError:
            raise UserInputError('Authentication failed')
        except Exception:
            raise UserInputError('Wrong Credentials invalid token')

    def update(self, token, template_name, subject, body, template_id):
        try:
            email = self.authorization.get_email(token)
            self.persistence_gateway.update(template_name, subject, body, email, template_id)
        except AuthenticationError:
            raise UserInputError('Authentication failed' )
        except InvalidOperation:
            raise UserInputError('Operation not allowed')

    def delete(self, token, template_id):
        try:
            email = self.authorization.get_email(token)
            self.persistence_gateway.delete(email, template_id)
        except AuthenticationError:
            raise UserInputError('Authentication failed' )
        except InvalidOperation:
            raise UserInputError('Operation not allowed')
