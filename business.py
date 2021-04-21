from flask import Flask, jsonify, request
from authorization import Authorization
import jwt

users = {}
tx = Authorization()
checker = "hghfg"


class Business:
    def __init__(self, persistence_gateway):
        self.persistence_gateway = persistence_gateway

    def register(self, r):
        payload = r.get_json()
        first_name = payload['first_name']
        last_name = payload['last_name']
        email = payload['email']
        password = payload['password']
        users[email] = password
        tx.add_users(email, password)
        return " ", 202

    def get_all(self, r):
        authorization_value = r.headers.get('Authorization')
        authorization_value = authorization_value[7:]
        key = "secret"
        credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")
        email = credentials["email"]
        temp = self.persistence_gateway.get(email, checker)
        return jsonify(temp), 202

    def insert(self, r):
        authorization_value = r.headers.get('Authorization')
        authorization_value = authorization_value[7:]
        key = "secret"
        credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")# try
        email = credentials["email"]
        if email in users.keys():
            mydict = {"name": "John", "address": "Highway 37", "_id": checker}
            self.persistence_gateway.add(email, mydict)
            print("donebngdhnjtgjhnfgjmfgjfgjfgjrtj")
            return credentials
        else:
            print("I am not allowed")
            return {'error': "access denied"}, 401

    def login(self, r):
        payload = r.get_json()
        email = payload['email']
        password = payload['password']
        print(tx.check_user(email, password))
        if users[email] == password:
            key = "secret"
            token = jwt.encode({"email": email, "password": password}, key, algorithm="HS256").decode("UTF-8")
            return jsonify({"token": token}), 202
        else:
            return {'error': "access denied"}, 401


