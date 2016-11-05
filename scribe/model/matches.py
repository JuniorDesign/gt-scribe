#represents the schema of the matches between the users who are notetakers and note-requestors
#every match contains a match id as pk, notetaker id, note-requestor id and a course id

from scribe import db
from scribe.model.base import BaseModel
from scribe.model.file import File
from scribe.model.course import Course

class Matches(BaseModel):
    __tablename__ = "matches"
    #id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, primary_key=True)
    notetaker_id = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    noterequester_id = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    course_id = db.Column(db.String(50), db.ForeignKey('course.course_id'), nullable=False)
    
    #Relationship specifying the course this match belongs to
    course = db.relationship('Course') 
    #Links course to the course table, it knows that the above FK for course.course_id corresponds to this
    #so it will find the course w this course_id

    # Relationship specifying the note taker for this match
    notetaker = db.relationship('User', foreign_keys=[notetaker_id], back_populates="taker_matches")
    #Using the given notetaker_id, it goes into taker_matches (the table for all matches with the corresponding notetaker) in user to find 
    #the notetaker in question

    # Relationship specifying the note requester for this match
    noterequester = db.relationship('User', foreign_keys=[noterequester_id], back_populates="requester_matches")
    #Using the given noterequester_id, goes to requester_matches and finds the user in question.
    
    #__table_args__ = (db.UniqueConstraint("username", "id", name = "unique_username_id"),)

    def __init__(self, notetaker_id, noterequester_id, course_id):
        self.notetaker_id = notetaker_id
        self.noterequester_id = noterequester_id
        self.course_id = course_id