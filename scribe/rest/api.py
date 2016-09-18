from scribe import db
from flask_restful import Resource
from scribe.repositories.userRepository import UserRepository


class HelloWorld(Resource):
	def get(self): #example of api
		return "hello world!"

class GetPassword(Resource):
	def __init__(self):
		self.userRepository = UserRepository()
	def get(self):
		print(self.userRepository.find(1))
