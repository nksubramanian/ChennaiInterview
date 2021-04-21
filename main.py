from flask import Flask, jsonify, request
import jwt
import pymongo
from persistence_gateway import PersistenceGateway
from business import Business

app = Flask(__name__)
storage = PersistenceGateway()

users = {}
t = Business()

@app.route("/register")
def register_function():
    t.register(request)
    payload = request.get_json()
    first_name = payload['first_name']
    last_name = payload['last_name']
    email = payload['email']
    password = payload['password']
    users[email] = password
    print(users)
    return jsonify({'first_name': first_name,
                    "last_name": last_name,
                    'email': email,
                    'password': password}), 202


@app.route("/login")
def login_function():
    return t.login(request)



@app.route("/checking")
def get_function():
    return t.get(request)
    #authorization_value = request.headers.get('Authorization')
    #authorization_value = authorization_value[7:]
    #key = "secret"
    #credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")
    #email = credentials["email"]
    #temp = storage.get(email, 28)
    #return jsonify(temp), 202



@app.route("/template")
def update_function():
    return t.update(request)
    #authorization_value = request.headers.get('Authorization')
    #authorization_value = authorization_value[7:]
    #key = "secret"
    #credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")# try
    #email = credentials["email"]
    #if email in users.keys():
        #mydict = {"name": "John", "address": "Highway 37", "_id": 77}
        #storage.add(email, mydict)
        #print("donebngdhnjtgjhnfgjmfgjfgjfgjrtj")
        #return credentials
    #else:
        #print("I am not allowed")
        #return {'error': "access denied"}, 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
