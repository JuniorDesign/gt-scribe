#represents the schema of enrollment
#each enrollment contains a username indicating the student and a course that the student is taking

from scribe import db
from scribe.model.base import BaseModel

class Enrollment(BaseModel):
    __tablename__ = "enrollment"
    username = db.Column(db.String(50), db.ForeignKey('user.username'), primary_key=True, nullable=False)
    course_id = db.Column(db.String(50), primary_key=True, nullable=False)

    def __init__(self, username, course_id):
        self.username = username
        self.course_id = course_id