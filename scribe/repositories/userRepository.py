from scribe.model.user import User
from scribe.repositories.baseRepository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super(UserRepository, self).__init__(User)

    def add_or_update(self, entity):
        return super(UserRepository, self).add_or_update(entity)
