from flask import Flask, jsonify, request
import jwt

app = Flask(__name__)

credentials = {}


@app.route("/register")
def register_function():
    payload = request.get_json()
    first_name = payload['first_name']
    last_name = payload['last_name']
    email = payload['email']
    password = payload['password']
    credentials[email] = password
    return jsonify({'first_name': first_name,
                    "last_name": last_name,
                    'email': email,
                    'password': password}), 202


@app.route("/login")
def login_function():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    if credentials[email] != password:
        return {'error': "access denied"}, 401
    else:
        key = "secret"
        token = jwt.encode({"email": email, "password": password}, key, algorithm="HS256").decode("UTF-8")
        return jsonify({"token": token}), 202


@app.route("/template")
def update_function():
    return jsonify({"token": ""}), 202




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
