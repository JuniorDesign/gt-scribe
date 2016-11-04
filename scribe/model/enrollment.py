#represents the schema of enrollment
#each enrollment contains a username indicating the student and a course that the student is taking

from scribe import db
from scribe.model.base import BaseModel

class Enrollment(BaseModel):
    __tablename__ = "enrollment"
    enrollment_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    course_id = db.Column(db.String(50), db.ForeignKey('course.course_id'), nullable=False)

    course = db.relationship('Course') 
    user = db.relationship('User')

    def __init__(self, username, course_id):
        self.username = username
        self.course_id = course_id