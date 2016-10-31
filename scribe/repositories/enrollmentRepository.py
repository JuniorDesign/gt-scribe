from scribe.model.enrollment import Enrollment
from scribe.repositories.baseRepository import BaseRepository

class EnrollmentRepository(BaseRepository):
        def __init__(self):
        	print("enrollment created")
            super(EnrollmentRepository, self).__init__(Enrollment)