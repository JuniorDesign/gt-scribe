#represents the schema of file storage
#each file contains a username indicating the student and a course that the student is taking

from scribe import db
from scribe.model.base import BaseModel

class File(BaseModel):
    __tablename__ = "file"
    file_id = db.Column(db.String(256), primary_key=True, nullable=False)
    file_name = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    notetaker_id = db.Column(db.String(50), db.ForeignKey('matches.notetaker_id'), nullable=False)
    course_id = db.Column(db.String(50), db.ForeignKey('matches.course_id'), nullable=False)

    def __init__(self, file_id, file_name, timestamp, notetaker_id, course_id):
    	self.file_id = file_id
    	self.file_name = file_name
    	self.timestamp = timestamp
    	self.notetaker_id = notetaker_id
    	self.course_id = course_id