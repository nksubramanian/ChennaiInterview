from flask import Flask, jsonify, request
import jwt
from business import Business
from persistence_gateway import PersistenceGateway
from authorization import Authorization
import pymongo


app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
templates_db = myclient["mydatabase"]
authorization = Authorization()
persistence_gateway = PersistenceGateway(templates_db)
t = Business(persistence_gateway, authorization)


@app.route("/register", methods=['POST'])
def register_function():
    payload = request.get_json()
    first_name = payload['first_name']
    last_name = payload['last_name']
    email = payload['email']
    password = payload['password']
    t.register(email, password, first_name, last_name)
    return "", 202

@app.route("/login", methods=['POST'])
def login_function():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    token = authorization.check_user_credentials(email, password)
    return jsonify({"token": token}), 202

@app.route("/template", methods=['POST'])
def insert_function():
    authorization_value = request.headers.get('Authorization')
    email = authorization.authorize_user(authorization_value) #returns null if tampered
    payload = request.get_json()
    x = t.insert(email, payload)
    return {'template_id': x}, 200


@app.route("/template/<template_id>", methods=['GET'])
def get_function(template_id):
    authorization_value = request.headers.get('Authorization')
    email = authorization.authorize_user(authorization_value)
    x = t.get(template_id, email)
    return jsonify(x)


@app.route("/template", methods=['GET'])
def get_all_function():
    authorization_value = request.headers.get('Authorization')
    email = authorization.authorize_user(authorization_value)
    temp = t.get_all(email)
    return jsonify(temp), 202

@app.route("/template/<template_id>", methods=['PUT'])
def update_function(template_id):
    authorization_value = request.headers.get('Authorization')
    email = authorization.authorize_user(authorization_value)
    payload = request.get_json()
    x = t.update(email, payload, template_id)
    return jsonify(x)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
