from flask import Flask, jsonify, request
app = Flask(__name__)

credentials = {}

@app.route("/register")
def create_audio_file():
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
def ccc():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    if credentials[email] = password


    #return jsonify({'room_id': xxx, "second": xxx}), 202
    #print("I am here")
    #print(credentials)
    #return jsonify(credentials), 202




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
