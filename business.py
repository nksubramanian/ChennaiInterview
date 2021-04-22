from flask import jsonify
from authorization import Authorization
import jwt

details = {}


class Business:
    def __init__(self, persistence_gateway, authorization):
        self.persistence_gateway = persistence_gateway
        self.authorization = authorization

    def register(self, email, password, first_name, last_name):
        details[email] = [first_name, last_name]
        self.authorization.add_users(email, password)
        print(details)

    def login(self, email, password):
        return self.authorization.check_user_credentials(email, password)

    def get_all(self, token):
        email = self.authorization.get_email(token)
        temp = self.persistence_gateway.get_all(email)
        return temp

    def insert(self, token, template_name, subject, body):
        email = self.authorization.get_email(token)
        payload = {'template_name': template_name, 'subject': subject, 'body': body, 'email': email}
        x = self.persistence_gateway.add(payload)
        return x

    def get(self, template_id, token):
        email = self.authorization.get_email(token)
        x = self.persistence_gateway.get(template_id, email)
        return x

    def update(self, email, payload, template_id):
        payload['email'] = email
        x = self.persistence_gateway.update(payload, template_id)

    def delete(self, email, template_id):
        x = self.persistence_gateway.delete(email, template_id)



