from scribe.model.matches import Matches
from scribe.repositories.baseRepository import BaseRepository

class MatchesRepository(BaseRepository):
        def __init__(self):
            super(MatchesRepository, self).__init__(Matches)

        def add_or_update(self, entity):
            return super(MatchesRepository, self).add_or_update(entity)

        def get_unmatched_users(self, course_id, usernames):
            usernamesWithMatches =  [match.noterequester_id for match in Matches.query.filter(Matches.noterequester_id.in_(usernames)).filter(Matches.course_id==course_id)]
            print("Username w matches: "+str(usernamesWithMatches))
            return [username for username in usernames if username not in usernamesWithMatches]

        def get_matched_users(self, course_id, usernames):
            usernamesWithMatches =  [match.noterequester_id for match in Matches.query.filter(Matches.noterequester_id.in_(usernames)).filter(Matches.course_id==course_id)]
            print("Username w matches: "+str(usernamesWithMatches))
            return [username for username in usernames if username in usernamesWithMatches]

        def get_matches_for_notetaker(self, username):
            matches = super(MatchesRepository, self).get(notetaker_id = username)
            print(matches)
            return matches

        def get_matches_for_noterequester(self, username):
            matches = super(MatchesRepository, self).get(noterequester_id = username)
            return matches

        def get_matches(self):
            matches = super(MatchesRepository, self).get()
            return matches