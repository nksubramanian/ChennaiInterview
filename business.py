from flask import Flask, jsonify, request
import jwt
from persistence_gateway import PersistenceGateway
import pymongo

users = {}
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
persistence_gateway = PersistenceGateway(mydb)

class Business:
    def __init__(self):
        self.a = 5

    def register(self, r):
        payload = r.get_json()
        first_name = payload['first_name']
        last_name = payload['last_name']
        email = payload['email']
        password = payload['password']
        users[email] = password

        return jsonify({'first_name': first_name,
                        "last_name": last_name,
                        'email': email,
                        'password': password}), 202

    def get(self, r):
        authorization_value = r.headers.get('Authorization')
        authorization_value = authorization_value[7:]
        key = "secret"
        credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")
        email = credentials["email"]
        temp = persistence_gateway.get(email, 1111)
        return jsonify(temp), 202

    def update(self, r):
        authorization_value = r.headers.get('Authorization')
        authorization_value = authorization_value[7:]
        key = "secret"
        credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")# try
        email = credentials["email"]
        if email in users.keys():
            mydict = {"name": "John", "address": "Highway 37", "_id": 1111}
            persistence_gateway.add(email, mydict)
            print("donebngdhnjtgjhnfgjmfgjfgjfgjrtj")
            return credentials
        else:
            print("I am not allowed")
            return {'error': "access denied"}, 401

    def login(self, r):
        payload = r.get_json()
        email = payload['email']
        password = payload['password']
        if users[email] == password:
            key = "secret"
            token = jwt.encode({"email": email, "password": password}, key, algorithm="HS256").decode("UTF-8")
            return jsonify({"token": token}), 202
        else:
            return {'error': "access denied"}, 401


