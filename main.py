from flask import Flask, jsonify, request
import jwt
import pymongo
from persistence_gateway import PersistenceGateway

app = Flask(__name__)
storage = PersistenceGateway()

users = {}


@app.route("/register")
def register_function():
    payload = request.get_json()
    first_name = payload['first_name']
    last_name = payload['last_name']
    email = payload['email']
    password = payload['password']
    users[email] = password
    return jsonify({'first_name': first_name,
                    "last_name": last_name,
                    'email': email,
                    'password': password}), 202


@app.route("/login")
def login_function():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    if users[email] != password:
        return {'error': "access denied"}, 401
    else:
        key = "secret"
        token = jwt.encode({"email": email, "password": password}, key, algorithm="HS256").decode("UTF-8")
        return jsonify({"token": token}), 202


@app.route("/ftemplate")
def fupdate_function():
    authorization_value = request.headers.get('Authorization')
    authorization_value = authorization_value[7:]
    key = "secret"
    credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")
    email = credentials["email"]
    if users[email] == credentials["password"]:
        mydict = {"name": "John", "address": "Highway 37", "_id": 99}
        print("I am here111")
        storage.add(email, mydict)
        return credentials
    else:
        return {'error': "access denied"}, 401


@app.route("/checking")
def return_function():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]
    x = mycol.find_one({'_id': 65})
    print("here i am")
    print(x)
    return x



@app.route("/template")
def update_function():
    authorization_value = request.headers.get('Authorization')
    authorization_value = authorization_value[7:]
    key = "secret"
    credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")
    email = credentials["email"]
    print("sgsagsa")
    print(email)
    if users[email] == credentials["password"]:
        mydict = {"name": "John", "address": "Highway 37", "_id": 97}
        storage.add(email, mydict)
        return credentials
    else:
        return {'error': "access denied"}, 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
