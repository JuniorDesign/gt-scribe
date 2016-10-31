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
        dbUser = UserRepository().get_account_type(session.get('username'))
        if dbUser is not None: #old cookie may exist but db may not be up-to-date
            g.user = {
                'name': session.get('username'),
                'type': dbUser.lower()
            }
        else:
            session.clear()

@app.route('/')
def index():
    if g.user:
        return render_template(g.user['type'] + '.html')
    return render_template('index.html')

@app.route('/taker/notes')
def notes():
    if g.user:
        return render_template('notes.html')
    return redirect(url_for('index'))

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
    session.pop('username', None) #maybe we can do session.clear() instead?
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
api.add_resource(scribe_api.CourseSubject, '/api/courses/<course_subject>')
api.add_resource(scribe_api.CourseNumber, '/api/courses/<course_subject>/<course_number>')
api.add_resource(scribe_api.CourseSection, '/api/courses/<course_subject>/<course_number>/<course_section>') #may not actually use this one
api.add_resource(scribe_api.TakerNotes, '/api/taker/notes')
#'/api/reservation/<string:reservation_id>') #example of using string params

