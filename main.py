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
template_service = Business(persistence_gateway, authorization)


@app.route("/register", methods=['POST'])
def register():
    payload = request.get_json()
    first_name = payload['first_name']
    last_name = payload['last_name']
    email = payload['email']
    password = payload['password']
    template_service.register(email, password, first_name, last_name)
    return "", 202

@app.route("/login", methods=['POST'])
def login():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    token = template_service.login(email, password)
    return jsonify({"token": token}), 202

@app.route("/template", methods=['POST'])
def insert():
    token = request.headers.get('Authorization')
    payload = request.get_json()
    template_name = payload['template_name']
    subject = payload['subject']
    body = payload['body']
    x = template_service.insert(token, template_name, subject, body)
    return {'template_id': x}, 200


@app.route("/template/<template_id>", methods=['GET'])
def get(template_id):
    token = request.headers.get('Authorization')
    x = template_service.get(template_id, token)
    return jsonify(x), 200


@app.route("/template", methods=['GET'])
def get_all():
    token = request.headers.get('Authorization')
    temp = template_service.get_all(token)
    return jsonify(temp), 202

@app.route("/template/<template_id>", methods=['PUT'])
def update(template_id):
    token = request.headers.get('Authorization')
    payload = request.get_json()
    template_name = payload['template_name']
    subject = payload['subject']
    body = payload['body']
    template_service.update(token, template_name, subject, body, template_id)
    return {'message': "successful"}, 200


@app.route("/template/<template_id>", methods=['DELETE'])
def delete(template_id):
    token = request.headers.get('Authorization')
    template_service.delete(token, template_id)
    return {'message': "successful"}, 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
