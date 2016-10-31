from scribe.model.matches import Matches
from scribe.repositories.baseRepository import BaseRepository

class MatchesRepository(BaseRepository):
        def __init__(self):
        	print("matches created")
            super(MatchesRepository, self).__init__(Matches)