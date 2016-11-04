from scribe.model.enrollment import Enrollment
from scribe.repositories.baseRepository import BaseRepository
from scribe.model.user import User

class EnrollmentRepository(BaseRepository):
        def __init__(self):
            super(EnrollmentRepository, self).__init__(Enrollment)

        def add_or_update(self, entity):
            return super(EnrollmentRepository, self).add_or_update(entity)

        def course_already_registered(self, username, course_id):
        	enrollment = super(EnrollmentRepository, self).get(username = username, course_id = course_id)
        	if len(enrollment) > 0:
        		return True
        	return False

        def get_enrollments_of_opposite_type(self, userType, course_id):
        	oppType = ""
        	if userType == "REQUESTER":
        		oppType = "TAKER"
        	elif userType == "TAKER":
        		oppType = "REQUESTER"
        	else:
        		return None
        	enrollments = [enrollment for enrollment in Enrollment.query.filter(course_id == Enrollment.course_id).group_by(Enrollment.enrollment_id) if enrollment.user.type == oppType]

        	return enrollments