#handles the routing for our application running on the local server (see serve.py in the root-level directory)

from scribe import app, db
from scribe.repositories.userRepository import UserRepository
from scribe.rest import api as scribe_api

from flask import g, redirect, render_template, session, url_for
from flask_restful import Api

api = Api(app)

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = {
            'name': session.get('username'),
            'type': UserRepository().get_account_type(session.get('username')).lower()
        }

@app.route('/')
def index():
    if g.user:
        return render_template(g.user['type'] + '.html')
    return render_template('index.html')

@app.route('/register')
def register_user():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register/success')
def loggedin():
    return render_template('register-success.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/adminview')
def admin_view():
    userRepository = UserRepository()
    users = userRepository.get_users_by_account_type("TAKER")
    return render_template('admin-view.html', users=users)

#example set up from my last project
api.add_resource(scribe_api.HelloWorld, '/api/helloworld') #example of making the api
api.add_resource(scribe_api.UserRegistration, '/api/register')
api.add_resource(scribe_api.UserLogin, '/api/login')
#'/api/reservation/<string:reservation_id>') #example of using string params

