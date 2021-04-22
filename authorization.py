import jwt


class Authorization:
    users = {}

    def __init__(self):
        pass

    def add_users(self, email, password):
        x = self.users[email] = password
        print(x)

    def check_user_credentials(self, email, password ):
        if self.users[email] == password:
            key = "secret"
            token = jwt.encode({"email": email}, key, algorithm="HS256").decode("UTF-8")
            return token

    def get_claim(self, authorization_value):
        key = "secret"
        credentials = jwt.decode(authorization_value, key, verify=True, algorithm="HS256") # try
        return credentials

    def authorize_user(self, authorization_value):
        key = "secret"
        authorization_value = authorization_value[7:]
        claim = self.get_claim(authorization_value)
        email = claim["email"]
        if authorization_value == jwt.encode({"email": email}, key, algorithm="HS256").decode("UTF-8"):
            return email #else returns null







