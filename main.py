from flask import Flask, jsonify, request
from business import Business
from business import UserInputError
from persistence_gateway import TemplateRepository, UserRepository
from authorization import Authorization
import pymongo


app = Flask(__name__)
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
templates_db = mongo_client["mydatabase"]
authorization = Authorization()
template_repository = TemplateRepository(templates_db)
user_repository = UserRepository(templates_db)
template_service = Business(template_repository, authorization, user_repository)


@app.route("/register", methods=['POST'])
def register():
    try:
        record = request.get_json()
        first_name = record['first_name']
        last_name = record['last_name']
        email = record['email']
        password = record['password']
        template_service.register(email, password, first_name, last_name)
    except UserInputError as error:
        return error.args[0], 400
    except Exception as error:
        return error.args[0], 500
    return "", 202


@app.route("/login", methods=['POST'])
def login():
    try:
        record = request.get_json()
        email = record['email']
        password = record['password']
        token = template_service.login(email, password)
    except UserInputError as error:
        return error.args[0], 400
    except Exception as error:
        return error.args[0], 500
    return jsonify({"token": token}), 202


@app.route("/template", methods=['POST'])
def insert():
    try:
        token = get_token(request)
        record = request.get_json()
        template_name = record['template_name']
        subject = record['subject']
        body = record['body']
        x = template_service.insert(token, template_name, subject, body)
        return {'template_id': x}, 200
    except UserInputError as error:
        return error.args[0], 400
    except Exception as error:
        return error.args[0], 500



@app.route("/template/<template_id>", methods=['GET'])
def get(template_id):
    try:
        token = get_token(request)
        x = template_service.get(template_id, token)
        return jsonify(x), 200
    except UserInputError as error:
        return error.args[0], 400
    except Exception as error:
        return error.args[0], 500




@app.route("/template", methods=['GET'])
def get_all():
    try:
        token = get_token(request)
        temp = template_service.get_all(token)
        return jsonify(temp), 202
    except UserInputError as error:
        return error.args[0], 400
    except Exception as error:
        return error.args[0], 500




@app.route("/template/<template_id>", methods=['PUT'])
def update(template_id):
    try:
        token = get_token(request)
        record = request.get_json()
        template_name = record['template_name']
        subject = record['subject']
        body = record['body']
        template_service.update(token, template_name, subject, body, template_id)
        return {'message': "successful"}, 200
    except UserInputError as error:
        return error.args[0], 400
    except Exception as error:
        return error.args[0], 500


@app.route("/template/<template_id>", methods=['DELETE'])
def delete(template_id):
    token = get_token(request)
    template_service.delete(token, template_id)
    return {'message': "successful"}, 200


def get_token(request_):
    authorization_value = request_.headers.get('Authorization')
    token = authorization_value[7:]
    return token


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
