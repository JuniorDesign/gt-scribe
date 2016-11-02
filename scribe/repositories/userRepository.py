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

        # Grabs the collection of users based on their account type
        # accountType must be ADMIN, REQUESTER, or TAKER
        def get_users_by_account_type(self, accountType):
            users = super(UserRepository, self).get(type = accountType)
            return users

        # Helper method to grab users of a specific type and with certain approval
        def get_users_by_account_type_and_approval(self, accountType, isApproved):
            users = super(UserRepository, self).get(type = accountType, approved = isApproved)
            return users

        # Grabs the approved note takers
        def get_approved_note_takers(self):
            users = get_users_by_account_type_and_approval("TAKER", True)
            return users

        # Grabs the unapproved note takers
        def get_unapproved_note_takers(self):
            users = get_users_by_account_type_and_approval("TAKER", False)
            return users

        # Grabs the approved note requesters
        def get_approved_note_requestors(self):
            users = get_users_by_account_type_and_approval("REQUESTER", True)
            return users

        # Grabs the unapproved note requesters
        def get_unapproved_note_requesters(self):
            users = get_users_by_account_type_and_approval("REQUESTER", False)
            return users

