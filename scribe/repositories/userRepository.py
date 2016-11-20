from scribe.model.user import User
from scribe.repositories.baseRepository import BaseRepository

class UserRepository(BaseRepository):
        def __init__(self):
            super(UserRepository, self).__init__(User)

        def add_or_update(self, entity):
            return super(UserRepository, self).add_or_update(entity)

        # Checks if the user exists in the db based on their username
        # Returns true if the user exists, false otherwise
        def user_exists(self, username):
            user = super(UserRepository, self).find(username)
            if user:
                return True
            return False

        # Checks if the username and password match in the database
        # Used for login
        # Returns true if valid credentials, false otherwise
        def check_username_and_password(self, username, password):
            user = super(UserRepository, self).find(username)
            if user:
                return user.check_password(password)
            return False

        # Grabs the account type of the user based on their username.
        # Returns the type if successful (ADMIN, REQUESTER, TAKER)
        # Returns None otherwise
        def get_account_type(self, username):
            user = super(UserRepository, self).find(username)
            if user:
                return user.type
            return None

        # Grabs the first_name of user
        def get_first_name(self, username):
            user = super(UserRepository, self).find(username)
            if user:
                return user.first_name
            return None

        # Grabs the collection of users based on their account type
        # accountType must be ADMIN, REQUESTER, or TAKER
        def get_users_by_account_type(self, accountType):
            users = super(UserRepository, self).get(type = accountType)
            return users

        # Helper method to grab users of a specific type and with certain approval
        def get_users_by_account_type_and_approval(self, accountType, isApproved):
            users = super(UserRepository, self).get(type = accountType, approved = isApproved)
            return users