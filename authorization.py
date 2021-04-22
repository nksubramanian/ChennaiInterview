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

    def _decode(self, authorization_value):
        key = "secret"
        claim = jwt.decode(authorization_value, key, verify=True, algorithm="HS256") # try
        return claim

    def get_email(self, authorization_value):
        authorization_value = authorization_value[7:]
        claim = self._decode(authorization_value)
        email = claim["email"]
        return email







