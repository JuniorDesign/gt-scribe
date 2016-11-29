from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError
 
class FeedbackForm(Form):
	first_name = TextField("First Name", [validators.Required("Please enter your first name.")])
	last_name = TextField("Last Name", [validators.Required("Please enter your last name.")])
	email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please ensure that the email address is valid.")])
	subject = TextField("Subject", [validators.Required("Please enter a subject.")])
	message = TextAreaField("Message", [validators.Required("Please enter some feedback.")])
	submit = SubmitField("Send")