from scribe.model.matches import Matches
from scribe.repositories.baseRepository import BaseRepository

class MatchesRepository(BaseRepository):
        def __init__(self):
            super(MatchesRepository, self).__init__(Matches)

        def add_or_update(self, entity):
            return super(MatchesRepository, self).add_or_update(entity)

        def get_unmatched_users(self, course_id, usernames):
        	usernamesWithMatches =  [match.noterequester_id for match in Matches.query.filter(Matches.noterequester_id.in_(usernames))]
        	return [username for username in usernames if username not in usernamesWithMatches]