from flask import Flask, jsonify, request
import jwt
from business import Business
from persistence_gateway import PersistenceGateway
import pymongo


app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
persistence_gateway = PersistenceGateway(mydb)
t = Business(persistence_gateway)


@app.route("/register", methods=['POST'])
def register_function():
    return t.register(request)


@app.route("/login", methods=['POST'])
def login_function():
    return t.login(request)



@app.route("/checking")
def get_all_function():
    return t.get_all(request)


@app.route("/template", methods=['POST'])
def insert_function():
    return t.insert(request)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
