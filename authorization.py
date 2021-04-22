import jwt


class Authorization:
    def __init__(self):
        pass

    def get_token(self, email):
        key = "secret"
        token = jwt.encode({"email": email}, key, algorithm="HS256").decode("UTF-8")
        return token

    def _decode(self, authorization_value):
        key = "secret"
        claim = jwt.decode(authorization_value, key, verify=True, algorithm="HS256")
        return claim

    def get_email(self, authorization_value):
        claim = self._decode(authorization_value)
        email = claim["email"]
        return email
