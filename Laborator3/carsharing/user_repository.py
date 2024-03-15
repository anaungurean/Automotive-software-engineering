class UserRepository:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def find_user_by_username(self, username):
        return next((user for user in self.users if user.username == username), None)

    def find_user_by_id(self, user_id):
        return next((user for user in self.users if user.id == user_id), None)
