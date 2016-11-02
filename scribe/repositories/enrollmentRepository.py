from scribe.model.enrollment import Enrollment
from scribe.repositories.baseRepository import BaseRepository

class EnrollmentRepository(BaseRepository):
        def __init__(self):
            super(EnrollmentRepository, self).__init__(Enrollment)

        def add_or_update(self, entity):
            return super(EnrollmentRepository, self).add_or_update(entity)

        def course_already_registered(self, username, course_id):
        	return False