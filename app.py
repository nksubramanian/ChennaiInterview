from flask import Flask, jsonify, request
from business_errors import UserInputError


def create_app(service):
    app = Flask(__name__)
    app.service = service

    @app.route("/register", methods=['POST'])
    def register():
        try:
            record = request.get_json()
            first_name = record['first_name']
            last_name = record['last_name']
            email = record['email']
            password = record['password']
            app.service.register(email, password, first_name, last_name)
        except UserInputError as error:
            return error.args[0], 400
        except Exception as error:
            return error.args[0], 500
        return "", 200

    @app.route("/login", methods=['POST'])
    def login():
        try:
            record = request.get_json()
            email = record['email']
            password = record['password']
            token = app.service.login(email, password)
        except UserInputError as error:
            return error.args[0], 400
        except Exception as error:
            return error.args[0], 500
        return jsonify({"token": token}), 200

    @app.route("/template", methods=['POST'])
    def insert():
        try:
            token = get_token(request)
            record = request.get_json()
            template_name = record['template_name']
            subject = record['subject']
            body = record['body']
            x = app.service.insert(token, template_name, subject, body)
            return {'template_id': x}, 200
        except UserInputError as error:
            return error.args[0], 400
        except Exception as error:
            return error.args[0], 500

    @app.route("/template/<template_id>", methods=['GET'])
    def get(template_id):
        try:
            token = get_token(request)
            x = app.service.get(template_id, token)
            return jsonify(x), 200
        except UserInputError as error:
            return error.args[0], 400
        except Exception as error:
            return error.args[0], 500

    @app.route("/template", methods=['GET'])
    def get_all():
        try:
            token = get_token(request)
            temp = app.service.get_all(token)
            return jsonify(temp), 200
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
            app.service.update(token, template_name, subject, body, template_id)
            return "", 200
        except UserInputError as error:
            return error.args[0], 400
        except Exception as error:
            return error.args[0], 500

    @app.route("/template/<template_id>", methods=['DELETE'])
    def delete(template_id):
        try:
            token = get_token(request)
            app.service.delete(token, template_id)
            return "", 200
        except UserInputError as error:
            return error.args[0], 400
        except Exception as error:
            return error.args[0], 500

    def get_token(request_):
        authorization_value = request_.headers.get('Authorization')
        token = authorization_value[7:]
        return token

    return app
