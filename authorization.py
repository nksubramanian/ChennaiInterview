class Authorization:
    users = {}
    def __init__(self):
        pass

    def add_users(self, email, password):
        self.users[email] = password

    def check_user(self, email, password):
        if self.users[email] == password:
            return True
        else:
            return False






