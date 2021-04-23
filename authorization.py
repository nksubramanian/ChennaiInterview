import jwt


class AuthenticationError(Exception):
    pass


class Authorization:

    key = "secret"

    def __init__(self):
        pass

    def get_token(self, email):
        token = jwt.encode({"email": email}, self.key, algorithm="HS256").decode("UTF-8")
        return token

    def __decode(self, authorization_value):
        claim = jwt.decode(authorization_value, self.key, verify=True, algorithm="HS256")
        return claim

    def get_email(self, authorization_value):
        try:
            claim = self.__decode(authorization_value)
            email = claim["email"]
            if self.get_token(email) != authorization_value:
                raise AuthenticationError("Authentication failed")
            return email
        except Exception:
            raise AuthenticationError("Authentication failed")


