from user_repository import UserRepository
from user import Owner, Renter
import uuid

class AuthenticationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, username, password, name, user_type):
        if self.user_repository.find_user_by_username(username):
            return False, "User already registered!"

        if user_type == 'owner':
            user = Owner(username, password, name)
        elif user_type == 'renter':
            user = Renter(username, password, name)
        else:
            return False, "Invalid user type!"

        self.user_repository.add_user(user)
        return True, "User registered sucessfully!"

    def login(self, username, password):
        user = self.user_repository.find_user_by_username(username)
        if user and user.password == password:
            if isinstance(user, Owner):
                user_type = 'owner'
            elif isinstance(user, Renter):
                user_type = 'renter'
            else:
                user_type = 'unknown'
            return user, user_type
        return False, "Wrong username or password!"
