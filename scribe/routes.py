#handles the routing for our application running on the local server (see serve.py in the root-level directory)

from scribe import db
from scribe.rest import api as scribe_api
from scribe import app
from flask import render_template
from flask_restful import Api

api = Api(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register')
def register_user():
	return render_template('register.html')

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/requester')
def requester():
	return render_template('requester.html')

@app.route('/taker')
def taker():
	return render_template('taker.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register/success')
def loggedin():
	return render_template('register-success.html')


#example set up from my last project
api.add_resource(scribe_api.HelloWorld, '/api/helloworld') #example of making the api
api.add_resource(scribe_api.UserRegistration, '/api/register')
api.add_resource(scribe_api.UserLogin, '/api/login')
#'/api/reservation/<string:reservation_id>') #example of using string params
