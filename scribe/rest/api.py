from scribe import db
from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from scribe.model.user import User
from scribe.repositories.userRepository import UserRepository
from scribe.repositories.courseRepository import CourseRepository

from werkzeug.datastructures import FileStorage
import boto3
import random
import string


class HelloWorld(Resource):
	def get(self): #example of api
		return "Hello world!"

class UserRegistration(Resource):
	def __init__(self):
		self.reqparse = RequestParser() #this parses the JSON files that get posted via ajax
		self.reqparse.add_argument('username', type=str, required= True, help="GaTech Username is required to register", location='json')
		self.reqparse.add_argument('password', type=str, required= True, help="Password is required to register", location='json')
		self.reqparse.add_argument('firstName', type=str, required= True, help="First name is required to register", location='json')
		self.reqparse.add_argument('lastName', type=str, required= True, help="Last name is required to register", location='json')
		self.reqparse.add_argument('type', type=str, required= True, help="Type is required to register", location='json')
		super(UserRegistration, self).__init__()

	def post(self):
		args = self.reqparse.parse_args()
		#Taking the information from the registration form and assinging it to Python variables
		username = args['username']
		print("username is " + str(username))
		password = args['password']
		firstName = args['firstName']
		lastName = args['lastName']
		approved = True #approve users by default at this point
		print("approved " + str(password) + " " + str(firstName) + " " + str(lastName) + " " + str(approved))
		
		if args['type'] == "admin":
			accountType = "ADMIN"
		elif args['type'] == "requester":
			accountType = "REQUESTER"
		elif args['type'] == "taker":
			accountType = "TAKER"
		else: #this is how you set a response json and a response status code
			return {"error": "Account type is missing"}, 400

		userRepository = UserRepository()
		print("user repository reached")
		if userRepository.user_exists(username):
			return{"error": "An account with this username already exists"}, 400

		newUser = User(username, password, firstName, lastName, accountType, approved)
		print("new user created")
		userRepository.add_or_update(newUser)
		userRepository.save_changes()
		print("user has been added to the db!")

		return {"message": "Post to database was successful. New user registered."}


class UserLogin(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('username', type=str, required= True, help="GaTech Username is required to login", location='json')
		self.reqparse.add_argument('password', type=str, required= True, help="Password is required to login", location='json')
		super(UserLogin, self).__init__()

	def post(self):
		args = self.reqparse.parse_args()
		username = args['username']
		password = args['password']

		userRepository = UserRepository()
		if userRepository.check_username_and_password(username, password): #true if correct, false if bad credentials
			accountType = userRepository.get_account_type(username)
			session['username'] = username
			return {
				"message": "User has been logged in successfully.",
				"username": username,
				"accountType": accountType
				}
		return {"error": "This username and password combination is not valid."}, 401

class CourseSubject(Resource):
	def get(self, course_subject):
		self.course_subject = course_subject
		courseRepository = CourseRepository()
		courses = courseRepository.get(subject = course_subject)
		return [course.as_dict() for course in courses]

class CourseNumber(Resource):
	def get(self, course_subject, course_number):
		self.course_subject = course_subject
		self.course_number = course_number
		courseRepository = CourseRepository()
		courses = courseRepository.get(subject = course_subject, course_number = course_number)
		return [course.as_dict() for course in courses]

#we may not actually use this one
class CourseSection(Resource):
	def get(self, course_subject, course_number, course_section):
		self.course_subject = course_subject
		self.course_number = course_number
		self.course_section = course_section
		courseRepository = CourseRepository()
		courses = courseRepository.get(subject = course_subject, course_number = course_number, section = course_section)
		return [course.as_dict() for course in courses]

class TakerNotes(Resource):

	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('file', location='files', type=FileStorage, required=True)
		super(TakerNotes, self).__init__()

	def post(self):
		args = self.reqparse.parse_args()
		file = args['file']
		filename = file.filename
		
		s3 = boto3.resource('s3')
		key = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(20)) + '__' + filename
		s3.Bucket('gt-scribe').put_object(Key=key, Body=file)		