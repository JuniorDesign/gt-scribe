#handles the routing for our application running on the local server (see serve.py in the root-level directory)

from scribe import app, db
from scribe.repositories.userRepository import UserRepository
from scribe.repositories.courseRepository import CourseRepository
from scribe.repositories.enrollmentRepository import EnrollmentRepository
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
        username = session['username']

        courseRepository = CourseRepository()
        subjects = courseRepository.get_distinct_subjects()

        userRepository = UserRepository()
        user = userRepository.find(username)
        myCourses = [e.course for e in user.enrollment]
        #this automatically joins users and enrollment table since we defined a relationship in user for enrollment
        #this will automatically join the course table w the enrollment table mentioned above since we defined the relationship in the enrollment model
        return render_template(g.user['type'] + '.html', subjects=subjects, myCourses = myCourses)
    return render_template('index.html')

@app.route('/taker/notes')
def notes():
    if g.user:
        return render_template('notes.html')
    return redirect(url_for('index'))

@app.route('/register')
def register_user():
    if g.user:
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login')
def login():
    if g.user:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register/success')
def loggedin():
    if g.user:
        return redirect(url_for('index'))
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
#api.add_resource(scribe_api.CourseSubjectOnly, '/api/subjects')
api.add_resource(scribe_api.CourseRegistration, '/api/course/register')
api.add_resource(scribe_api.CourseNumbersOnly, '/api/courses/distinct/<course_subject>')
api.add_resource(scribe_api.CourseSectionsOnly, '/api/courses/distinct/<course_subject>/<course_number>')
api.add_resource(scribe_api.CourseByCrn, '/api/courses/crn/<crn>')
api.add_resource(scribe_api.CourseNumbersBySubject, '/api/courses/<course_subject>') #not really used, but nice for testing
api.add_resource(scribe_api.CoursesSectionsByNumberSubject, '/api/courses/<course_subject>/<course_number>') #not really used, but nice for testing
api.add_resource(scribe_api.Course, '/api/courses/<course_subject>/<course_number>/<course_section>') #may not actually use this one
api.add_resource(scribe_api.TakerNotes, '/api/taker/notes')
#'/api/reservation/<string:reservation_id>') #example of using string params

