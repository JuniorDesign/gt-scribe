#model of the user table/entity
#represents the schema for the user database
#all users have a username, password, first name, last name, type (admin or student), approved (t/f)

from scribe import db
from scribe.model.base import BaseModel

class User(BaseModel):
    __tablename__ = "user"
    #id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum("ADMIN", "REQUESTER", "TAKER"), nullable=False)
    approved = db.Column(db.Boolean)
    #Relationship A : 1 to many relationship between the user and matches tables
    #using the noterequestor's id, we find the notetakers matched
    #matches = db.relationship('matches', backref='user', lazy='dynamic')
    #Relationship B : 1 to many relationship between the user and enrollment tables
    #enrollment = db.relationship('enrollment', backref='user', lazy='dynamic')
    #__table_args__ = (db.UniqueConstraint("username", "id", name = "unique_username_id"),)


    def __init__(self, username, password, first_name, last_name, type, approved):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.type = type
        self.approved = approved
        print("user created")

