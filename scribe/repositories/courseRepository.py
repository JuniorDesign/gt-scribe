from scribe.model.course import Course
from scribe.repositories.baseRepository import BaseRepository

class CourseRepository(BaseRepository):
        def __init__(self):
        	print("course repo created")
            super(CourseRepository, self).__init__(Course)