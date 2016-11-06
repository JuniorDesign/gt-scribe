from scribe.model.feedback import Feedback
from scribe.repositories.baseRepository import BaseRepository

class FeedbackRepository(BaseRepository):
    def __init__(self):
    	print("feedback created")
    	super(FeedbackRepository, self).__init__(Feedback)

    def add_or_update(self, username, feedback_text):
    	feedback = Feedback(username, feedback_text)
    	return super(FeedbackRepository, self).add_or_update(feedback)