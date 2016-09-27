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
            users = super(UserRepository, self).get(username = username)
            return len(users) > 0

        # Checks if the username and password match in the database
        # Used for login
        # Returns true if valid credentials, false otherwise
        def check_username_and_password(self, username, password):
            users = super(UserRepository, self).get(username = username) #returns ALL users with this username (should be just 1)
            # If no user exists, will return empty (length of 0)
            if len(users) > 0:
                if users[0].password == password:
                    return True
            return False

        # Grabs the account type of the user based on their username.
        # Returns the type if successful (ADMIN, REQUESTER, TAKER)
        # Returns None otherwise
        def get_account_type(self, username):
            users = super(UserRepository, self).get(username = username) #returns ALL users with this username (should be just 1)
            # If no user exists, will return empty (length of 0)
            if len(users) > 0:
                if users[0].type != None:
                    print("Entered the condition " + users[0].type)
                    return users[0].type
            return None

        # Grabs the collection of users based on their account type
        # accountType must be ADMIN, REQUESTER, or TAKER
        def get_users_by_account_type(self, accountType):
            users = super(UserRepository, self).get(type = accountType)
            return users