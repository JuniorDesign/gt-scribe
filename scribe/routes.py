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
        userRepository = UserRepository()
        user = userRepository.find(username)
        userType = user.type

        matchedCourses = ""
        if userType == "TAKER":
            matchedCourses = [match.course for match in user.taker_matches]
        elif userType == "REQUESTER":
            matchedCourses = [match.course for match in user.requester_matches]
        else:
            render_template("admin.html", username=username)
        
        if len(matchedCourses) > 0: #if you have a match, you're taken to the match page instead
            return redirect(url_for('myClasses'))
        return redirect(url_for('enrollment')) #if you don't have any matches yet, you're back at the class enrollment page
    return render_template('index.html')

# Route for selecting courses you either need notes for, or you want to take notes for
# This route can be used by either taker or requester
# The pages are identical, but we use a different intro text based on the user type
@app.route('/enrollment')
def enrollment():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        userType = user.type
        if userType != "TAKER" and userType != "REQUESTER":
            render_template("admin.html", username=username)

        courseRepository = CourseRepository()
        subjects = courseRepository.get_distinct_subjects()
        myCourses = [e.course for e in user.enrollment]
        print(myCourses)
        return render_template('enrollment.html', username = username, userType = userType, subjects = subjects, myCourses = myCourses)
    return redirect(url_for('index'))

# Route for the matches that you have
# Page is the same for both takers and requesters
# Toggles text based on the user type
@app.route('/my-classes')
def myClasses():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        userType = user.type
        matchedCourses = ""
        if userType == "TAKER":
            matchedCourses = [match.course for match in user.taker_matches]
        elif userType == "REQUESTER":
            matchedCourses = [match.course for match in user.requester_matches]
        else:
            render_template("admin.html", username=username)

        return render_template('select-course.html', username = username, userType = userType, matchedCourses = matchedCourses)
    return redirect(url_for('index'))

@app.route('/notes/<int:course_id>')
def notes(course_id):
    if g.user:
        #Do security checks here to make sure only matching students get through this block#
        #don't want willynilly students trying to upload/download notes#
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        userType = user.type
        if userType == "ADMIN":
            redirect(url_for('admin'))
        return render_template('upload-download.html', username = username, userType = userType, course_id = course_id)
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

@app.route('/admin')
def admin():
    userRepository = UserRepository()
    users = userRepository.get_users_by_account_type("TAKER")
    return render_template('admin-view.html', users=users)

#example set up from my last project
api.add_resource(scribe_api.HelloWorld, '/api/helloworld') #example of making the api
api.add_resource(scribe_api.UserRegistration, '/api/register')
api.add_resource(scribe_api.UserLogin, '/api/login')
#api.add_resource(scribe_api.CourseSubjectOnly, '/api/subjects')
api.add_resource(scribe_api.Notes, '/api/notes')
api.add_resource(scribe_api.CourseRegistration, '/api/course/register')
api.add_resource(scribe_api.CourseNumbersOnly, '/api/courses/distinct/<course_subject>')
api.add_resource(scribe_api.CourseSectionsOnly, '/api/courses/distinct/<course_subject>/<course_number>')
api.add_resource(scribe_api.CourseByCrn, '/api/courses/crn/<crn>')
api.add_resource(scribe_api.CourseNumbersBySubject, '/api/courses/<course_subject>') #not really used, but nice for testing
api.add_resource(scribe_api.CoursesSectionsByNumberSubject, '/api/courses/<course_subject>/<course_number>') #not really used, but nice for testing
api.add_resource(scribe_api.Course, '/api/courses/<course_subject>/<course_number>/<course_section>') #may not actually use this one
#api.add_resource(scribe_api.Notes, '/api/notes')

