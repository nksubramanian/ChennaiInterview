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

    def get_all(self, r):
        authorization_value = r.headers.get('Authorization')
        authorization_value = authorization_value[7:]
        key = "secret"
        credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")
        email = credentials["email"]
        temp = self.persistence_gateway.get(email, checker)
        return jsonify(temp), 202

    def insert(self, email, payload):
        payload['email'] = email
        x = self.persistence_gateway.add(payload)
        return x

    def get(self, template_id, email):
        x = self.persistence_gateway.get(template_id, email)
        return x

