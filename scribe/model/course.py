#represents the schema of a course
#each course contains a course id, subject, course number, section and a crn number

from scribe import db
from scribe.model.base import BaseModel

class Course(BaseModel):
    __tablename__ = "course"
    course_id = db.Column(db.String(50), primary_key=True, nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    course_number = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)
    crn = db.Column(db.String(50), nullable=False)

    def __init__(self, course_id, subject, course_number, section, crn):
        print("course.py")
        self.course_id = course_id
        self.subject = subject
        self.course_number = course_number
        self.crn = crn