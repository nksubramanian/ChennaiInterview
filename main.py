from flask import Flask, jsonify, request
import jwt
import pymongo
from persistence_gateway import PersistenceGateway
from business import Business

app = Flask(__name__)

t = Business()

@app.route("/register")
def register_function():
    return t.register(request)


@app.route("/login")
def login_function():
    return t.login(request)



@app.route("/checking")
def get_function():
    return t.get(request)



@app.route("/template")
def update_function():
    return t.update(request)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
