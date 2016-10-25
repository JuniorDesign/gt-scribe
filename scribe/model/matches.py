#represents the schema of the matches between the users who are notetakers and note-requestors
#every match contains a match id as pk, notetaker id, note-requestor id and a course id

from scribe import db
from scribe.model.base import BaseModel
from scribe.model.file import File

class Matches(BaseModel):
    __tablename__ = "matches"
    #id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, primary_key=True)
    notetaker_id = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    noterequester_id = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    course_id = db.Column(db.String(50), nullable=False)
    files = db.relationship('File', backref='Matches', lazy='dynamic')
    #__table_args__ = (db.UniqueConstraint("username", "id", name = "unique_username_id"),)


    def __init__(self, match_id, notetaker_id, noterequester_id, course_id):
        print("matches.py")
        self.match_id = match_id
        self.notetaker_id = notetaker_id
        self.noterequester_id = noterequester_id
        self.course_id = course_id
