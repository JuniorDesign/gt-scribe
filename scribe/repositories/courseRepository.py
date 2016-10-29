from scribe.model.course import Course
from scribe.repositories.baseRepository import BaseRepository

class CourseRepository(BaseRepository):
        def __init__(self):
            print("course repo created")
            super(CourseRepository, self).__init__(Course)

        def add_or_update(self, entity):
            return super(CourseRepository, self).add_or_update(entity)