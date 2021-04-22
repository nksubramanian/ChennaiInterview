from flask import jsonify
from authorization import Authorization
import jwt

users = {}
tx = Authorization()
checker = "65"


class Business:
    def __init__(self, persistence_gateway, authorization_db):
        self.persistence_gateway = persistence_gateway
        self.authorization_db = authorization_db

    def register(self, email, password):
        users[email] = password
        self.authorization_db.add_users(email, password)

    def get_all(self, r):
        authorization_value = r.headers.get('Authorization')
        authorization_value = authorization_value[7:]
        key = "secret"
        credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")
        email = credentials["email"]
        temp = self.persistence_gateway.get(email, checker)
        return jsonify(temp), 202

    def insert(self, email, authorization_value, payload):
        payload['token'] = authorization_value
        x = self.persistence_gateway.add(payload)
        return x

    def login(self, r):
        if users[email] == password:
            key = "secret"
            token = jwt.encode({"email": email, "password": password}, key, algorithm="HS256").decode("UTF-8")
            return jsonify({"token": token}), 202
        else:
            return {'error': "access denied"}, 401

    def get(self, template_id, token):
        x = self.persistence_gateway.get(template_id, token)
        return x

