#represents the schema of feedback from the user
#each feedback entry contains the username, feedback and an identifier for that entry

from scribe import db
from scribe.model.base import BaseModel

class Feedback(BaseModel):
    __tablename__ = "feedback"
    feedback_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    feedback_text = db.Column(db.String(256), nullable=False)

    def __init__(self, username, feedback_text):
        self.username = username
        self.feedback_text = feedback_text