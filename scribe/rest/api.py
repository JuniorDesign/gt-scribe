from scribe import db
from flask_restful import Resource
from scribe.repositories.userRepository import UserRepository


class HelloWorld(Resource):
	def get(self): #example of api
		return "hello world!"

class GetPassword(Resource):
	def __init__(self):
		self.userRepository = UserRepository()
		variableName = userRepository().as_dict()
	def get(self):
		print(self.userRepository.find(1))

class UserRegistration(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('username', type=str, required= True, help="GaTech Username is required to register", location='json')
		self.reqparse.add_argument('password', type=str, required= True, help="Password is required to register", location='json')
		self.reqparse.add_argument('firstName', type=str, required= True, help="First name is required to register", location='json')
		self.reqparse.add_argument('lastName', type=str, required= True, help="Last name is required to register", location='json')
		self.reqparse.add_argument('type', type=str, required= True, help="Type is required to register", location='json')
		super(UserRegistration, self).__init__()

	def post(self): 
		args = self.reqparse.parse_args()
		username = args['username']
		password = args['password']
		firstName = args['firstName']
		lastName = args['lastName']
		accountType = args['type']
		approved = True

		#todo: post to db w this data

		#if not db.mysqldb.user_exists(username) and  not db.mysqldb.email_exists(email):
		#	db.mysqldb.register_user(username, email, password, firstName, lastName)
		#	return {"message": "User successfully created", "result": True}
		#else:
		#return {"error": "This user already exists", "result": False}, 400

