from flask import Flask, jsonify, request
import jwt
from business import Business
from persistence_gateway import PersistenceGateway
from authorization import Authorization
import pymongo


app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
templates_db = myclient["mydatabase"]
authorization_db = Authorization()
persistence_gateway = PersistenceGateway(templates_db)
t = Business(persistence_gateway, authorization_db)


@app.route("/register", methods=['POST'])
def register_function():
    payload = request.get_json()
    first_name = payload['first_name']
    last_name = payload['last_name']
    email = payload['email']
    password = payload['password']
    t.register(email, password)
    return "", 202



@app.route("/login", methods=['POST'])
def login_function():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    token = authorization_db.check_user_credentials(email, password)
    return jsonify({"token": token}), 202



@app.route("/checking")
def get_all_function():
    return t.get_all(request)


@app.route("/template", methods=['POST'])
def insert_function():
    authorization_value = request.headers.get('Authorization')
    authorization_value = authorization_value[7:]
    claim = authorization_db.get_claim(authorization_value)
    email = claim["email"]
    payload = request.get_json()
    x = t.insert(email, authorization_value, payload)
    return {'id': x}, 200


@app.route("/template/<template_id>", methods=['GET'])
def get_function(template_id):
    authorization_value = request.headers.get('Authorization')
    authorization_value = authorization_value[7:]
    x = t.get(template_id, authorization_value)
    return jsonify(x)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
