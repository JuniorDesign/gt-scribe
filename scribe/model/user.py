#model of the user table/entity
#represents the schema for the user database
#all users have a username, password, first name, last name, type (admin or student), approved (t/f)

from werkzeug.security import generate_password_hash, check_password_hash

from scribe import db
from scribe.model.base import BaseModel
from scribe.model.matches import Matches
from scribe.model.enrollment import Enrollment

class User(BaseModel):
    __tablename__ = "user"
    #id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), db.ForeignKey('user.username'), primary_key=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum("ADMIN", "REQUESTER", "TAKER"), nullable=False)
    approved = db.Column(db.Boolean)
    #Relationship A : 1 to many relationship between the user and matches tables
    #using the noterequestor's id, we find the notetakers matched

    #creates a collection of matches where the user in question is the notetaker
    #ie if you're a notetaker and you have 5 matches, then this will have those 5 match rows w/ this notetaker
    taker_matches = db.relationship('Matches', foreign_keys="Matches.notetaker_id")
    
    #creates a collection of matches where the user in question is the requester
    #ie if you're a requester and you have 5 notetakers for 5 diff classes, then this will have those 5 match rows w/ those notetakers
    requester_matches = db.relationship('Matches', foreign_keys="Matches.noterequester_id")

    #Relationship B : 1 to many relationship between the user and enrollment tables
    enrollment = db.relationship('Enrollment', backref='User', lazy='dynamic')
    #__table_args__ = (db.UniqueConstraint("username", "id", name = "unique_username_id"),)

    files = db.relationship('File')


    def __init__(self, username, password, email, first_name, last_name, type, approved):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.type = type
        self.approved = approved

    def check_password(self, password):
        return check_password_hash(self.password, password)
