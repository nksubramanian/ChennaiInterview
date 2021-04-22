from flask import jsonify
from authorization import Authorization
import jwt

details = {}


class Business:
    def __init__(self, template_repository, authorization):
        self.persistence_gateway = template_repository
        self.authorization = authorization

    def register(self, email, password, first_name, last_name):
        details[email] = [first_name, last_name]
        self.authorization.add_users(email, password)
        print(details)

    def login(self, email, password):
        return self.authorization.check_user_credentials(email, password)

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

        x = self.persistence_gateway.update(template_name, subject, body, email, template_id)

    def delete(self, token, template_id):
        email = self.authorization.get_email(token)
        x = self.persistence_gateway.delete(email, template_id)



