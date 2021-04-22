from flask import jsonify
from authorization import Authorization
import jwt

details = {}
tx = Authorization()
checker = "65"


class Business:
    def __init__(self, persistence_gateway, authorization_db):
        self.persistence_gateway = persistence_gateway
        self.authorization_db = authorization_db

    def register(self, email, password, first_name, last_name):
        details[email] = [first_name, last_name]
        self.authorization_db.add_users(email, password)
        print(details)

    def get_all(self, email):
        temp = self.persistence_gateway.get_all(email)
        return temp

    def insert(self, email, payload):
        payload['email'] = email
        x = self.persistence_gateway.add(payload)
        return x

    def get(self, template_id, email):
        x = self.persistence_gateway.get(template_id, email)
        return x

    def update(self, email, payload, template_id):
        payload['email'] = email
        x = self.persistence_gateway.update(payload, template_id)
        return x


