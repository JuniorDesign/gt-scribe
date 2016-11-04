from scribe import db
from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from scribe.model.user import User
from scribe.model.file import File
from scribe.repositories.userRepository import UserRepository
from scribe.repositories.courseRepository import CourseRepository
from scribe.repositories.fileRepository import FileRepository
from scribe.model.enrollment import Enrollment
from scribe.repositories.enrollmentRepository import EnrollmentRepository
from scribe.model.matches import Matches
from scribe.repositories.matchesRepository import MatchesRepository

from werkzeug.datastructures import FileStorage
import boto3
import random
import string
import datetime


class HelloWorld(Resource):
	def get(self): #example of api
		return "Hello world!"

class UserRegistration(Resource):
	def __init__(self):
		self.reqparse = RequestParser() #this parses the JSON files that get posted via ajax
		self.reqparse.add_argument('username', type=str, required= True, help="GaTech Username is required to register", location='json')
		self.reqparse.add_argument('password', type=str, required= True, help="Password is required to register", location='json')
		self.reqparse.add_argument('email', type=str, required= True, help="Email is required to register", location='json')
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
		email = args['email']
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
		if userRepository.user_exists(username):
			return{"error": "An account with this username already exists"}, 400

		newUser = User(username, password, email, firstName, lastName, accountType, approved)
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

class CourseRegistration(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('subject', type=str, required= True, help="Course subject is required to enroll in course", location='json')
		self.reqparse.add_argument('course_number', type=str, required= True, help="Course number is required to enroll in course", location='json')
		self.reqparse.add_argument('section', type=str, required= True, help="Course section is required to enroll in course", location='json')
		super(CourseRegistration, self).__init__()

	def post(self):
		args = self.reqparse.parse_args()
		if 'username' in session:
			username = session['username']
			subject = args['subject']
			course_number = args['course_number']
			section = args['section']
			enrollmentRepository = EnrollmentRepository()
			courseRepository = CourseRepository()
			course = courseRepository.get(subject = subject, course_number = course_number, section = section)[0]
			crn = course.course_id
			if enrollmentRepository.course_already_registered(username, crn):
				return {"error": "You have already registered for this course."}, 400
			enrollCourse = Enrollment(username, crn)
			enrollmentRepository.add_or_update(enrollCourse)
			enrollmentRepository.save_changes()
			#check for matches here
			userRepository = UserRepository()
			user = userRepository.find(username)
			userType = user.type
			matchesRepository = MatchesRepository()

			oppEnrollments = enrollmentRepository.get_enrollments_of_opposite_type(userType, crn)
			if oppEnrollments is not None and len(oppEnrollments) > 0:
				if userType == "REQUESTER":
					newMatch = Matches(oppEnrollments[0].username, username, crn)
					matchesRepository.add_or_update(newMatch)
				elif userType == "TAKER":
					unmatchedRequesters = matchesRepository.get_unmatched_users(crn, [oppEnrollment.username for oppEnrollment in oppEnrollments])
					for requester in unmatchedRequesters:
						print("New match for the requester: "+requester)
						newMatch = Matches(username, requester, crn)
						matchesRepository.add_or_update(newMatch)
					#match to all requesters who arent matched yet
				else:
					print("why are you here??")
					# fail here, return some error
				matchesRepository.save_changes()
			#check enrollment table for the crn
			# if crn exists, grab the username
			# check user table to see what the user type is of those usernames
			# if its the opposite of what you are, make a match and add it to the match table
			return {
				"message": "Course has been enrolled in successfully.",
				"username": username,
				"crn": crn
			}

		else:
			return {"error": "There is no currently logged in account."}, 401



#currently not used
class CourseSubjectOnly(Resource): #grabs distinct subjects
	def get(self):
		courseRepository = CourseRepository()
		return courseRepository.get_distinct_subjects()

class CourseNumbersOnly(Resource): #grabs distinct numbers
	def get(self, course_subject):
		courseRepository = CourseRepository()
		if courseRepository.subject_exists(course_subject):
			return courseRepository.get_distinct_course_number_for_subject(course_subject)
		return {"error": "The requested course subject is not valid."}, 404

class CourseSectionsOnly(Resource): #grabs all sections available for a course number/subject
	def get(self, course_subject, course_number):
		courseRepository = CourseRepository()
		if courseRepository.subject_exists(course_subject):
			if courseRepository.number_exists(course_subject, course_number):
				return courseRepository.get_course_sections(course_subject, course_number)
		return {"error": "The requested course subject and number are not valid together."}, 404

class CourseByCrn(Resource):
	def get(self, crn):
		courseRepository = CourseRepository()
		course = courseRepository.find(crn)
		if course:
			return course.as_dict()
		return {"error": "Couldn't find a course with the specified CRN."}, 404

#don't use currently, but convenient for testing
class CourseNumbersBySubject(Resource):
	def get(self, course_subject):
		courseRepository = CourseRepository()
		courses = courseRepository.get(subject = course_subject)
		return [course.as_dict() for course in courses]

#don't use currently, but convenient for testing
class CoursesSectionsByNumberSubject(Resource):
	def get(self, course_subject, course_number):
		courseRepository = CourseRepository()
		courses = courseRepository.get(subject = course_subject, course_number = course_number)
		return [course.as_dict() for course in courses]

#we may not actually use this one, but convenient for testing
class Course(Resource):
	def get(self, course_subject, course_number, course_section):
		courseRepository = CourseRepository()
		courses = courseRepository.get(subject = course_subject, course_number = course_number, section = course_section)
		return [course.as_dict() for course in courses]

class TakerNotes(Resource):
	def __init__(self):
		self.reqparse = RequestParser()
		self.reqparse.add_argument('file', location='files', type=FileStorage, required=True)
		self.reqparse.add_argument('user_id', type=str, required=True)
		self.reqparse.add_argument('course_id', type=str, required=True)
		super(TakerNotes, self).__init__()

	def post(self):
		#getting all arguments from request
		args = self.reqparse.parse_args()
		print(args)
		file = args['file']
		notetaker_id = args['user_id']
		course_id = args['course_id']
		file_name = file.filename
		file_id = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(20)) + '__' + file_name
		timestamp = datetime.datetime.now()

		#making a file object and db object
		newFile = File(file_id, file_name, timestamp, notetaker_id, course_id)
		fileRepository = FileRepository()
		print("new file created")
		fileRepository.add_or_update(newFile)
		fileRepository.save_changes()
		print("file has been added to the db!")

		#uploading to S3
		#s3 = boto3.resource('s3')
		#s3.Bucket('gt-scribe').put_object(Key=file_id, Body=file)

		return {"message": "Post to database was successful. New file added."}