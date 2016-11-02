from scribe.model.course import Course
from scribe.repositories.baseRepository import BaseRepository

class CourseRepository(BaseRepository):
        def __init__(self):
            super(CourseRepository, self).__init__(Course)

        def add_or_update(self, entity):
            return super(CourseRepository, self).add_or_update(entity)

        def subject_exists(self, subject):
        	return True

        def number_exists(self, course_subject, course_number):
        	return True

        def get_distinct_subjects(self):
        	distinctCourseSubjects = Course.query.group_by(Course.subject)
        	return  [course.subject for course in distinctCourseSubjects]

        def get_distinct_course_number_for_subject(self, subject):
        	distinctCourseNumbers = Course.query.filter_by(subject = subject).group_by(Course.course_number)
        	return [course.course_number for course in distinctCourseNumbers]

        def get_course_sections(self, subject, course_number):
        	courses = Course.query.filter_by(subject = subject, course_number = course_number).group_by(Course.section)
        	return [course.section for course in courses]

