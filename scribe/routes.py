#handles the routing for our application running on the local server (see serve.py in the root-level directory)

from scribe import app, db
from scribe.repositories.userRepository import UserRepository
from scribe.repositories.courseRepository import CourseRepository
from scribe.repositories.enrollmentRepository import EnrollmentRepository
from scribe.repositories.feedbackRepository import FeedbackRepository
from scribe.repositories.fileRepository import FileRepository
from scribe.repositories.matchesRepository import MatchesRepository
from scribe.rest import api as scribe_api

from flask import g, make_response, redirect, render_template, send_file, session, url_for
from flask_restful import Api
from flask import Flask, request, flash
from scribe.forms import FeedbackForm

from flask_mail import Message, Mail
import boto3
import botocore
import io

mail = Mail()

app.secret_key = 'development key'
api = Api(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'gburdell369@gmail.com'
app.config["MAIL_PASSWORD"] = 'GTjuniordesign'

mail.init_app(app)

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        dbUser = UserRepository().get_account_type(session.get('username'))
        first_name = UserRepository().get_first_name(session.get('username'))
        if dbUser is not None: #old cookie may exist but db may not be up-to-date
            g.user = {
                'name': session.get('username'),
                'firstName': first_name,
                'type': dbUser.lower()
            }
        else:
            session.clear()

# Route for the index page.
# Users without a login cookie are taken to the home page.
# Users with a login cookie are taken to the enrollment page or match page
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
            return redirect(url_for('admin'))
        
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
        courseRepository = CourseRepository()
        userType = user.type
        matchedCourses = ""
        if userType =="ADMIN":
            return redirect(url_for('admin'))
        if userType == "TAKER":
            matchedCoursesDupes = [match.course for match in user.taker_matches]
            matchedCourses = set(matchedCoursesDupes) #by using sets, we don't get duplicates
        elif userType == "REQUESTER":
            matchedCoursesDupes = [match.course for match in user.requester_matches]
            matchedCourses = set(matchedCoursesDupes)
        else:
            return redirect(url_for('index'))
        myCourses = [e.course for e in user.enrollment]
        unmatchedCourses = []
        for course in myCourses:
            if course not in matchedCourses:
                unmatchedCourses.append(course)
        return render_template('select-course.html', username = username, userType = userType, matchedCourses = matchedCourses, unmatchedCourses = unmatchedCourses, firstName = user.first_name)
    return redirect(url_for('index'))

# Route for the upload/download page for this course
@app.route('/notes/<int:course_id>')
def notes(course_id):
    if g.user:
        #Do security checks here to make sure only matching students get through this block#
        #don't want willynilly students trying to upload/download notes#
        courseRepository = CourseRepository()
        course = courseRepository.find(course_id)
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        userType = user.type
        if userType == "ADMIN":
            redirect(url_for('admin'))
        files = FileRepository().get_files_for_course(course_id)
        return render_template('upload-download.html', username = username, userType = userType, course=course, course_id = course_id, files=files)
    return redirect(url_for('index'))

@app.route('/notes/<course_id>/<key>', methods=['GET'])
def get_notes(course_id, key):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('gt-scribe')
    if g.user:
        file_to_download = FileRepository().get_file(key)
        if file_to_download.course_id == course_id and EnrollmentRepository().course_already_registered(g.user['name'], course_id): 
            try:
                data = io.BytesIO()
                bucket.download_fileobj(file_to_download.file_id, data)
                data.seek(0)
                return send_file(data, as_attachment=True, attachment_filename=file_to_download.file_name)
            except botocore.exceptions.ClientError as err:
                print(err)
                return None

        return "file not found"
    return redirect(url_for('index'))

# Route for user registration in the system
@app.route('/register')
def register_user():
    if g.user:
        return redirect(url_for('index'))
    return render_template('register.html')

# Route for logging in
@app.route('/login')
def login():
    if g.user:
        return redirect(url_for('index'))
    return render_template('login.html')

# Route for successful user registration
# Users must manually navigate back to the login screen
@app.route('/register/success')
def loggedin():
    if g.user:
        return redirect(url_for('index'))
    return render_template('register-success.html')

# Route for logging out
# clears the user cookie from their browser
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None) #maybe we can do session.clear() instead?
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        if user.type != "ADMIN":
            return redirect(url_for('index'))
        #users = userRepository.get_users_by_account_type("TAKER")
        return render_template('admin-view.html', username = username, userType = user.type)
    return redirect(url_for('index'))

@app.route('/admin/students')
def students():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        if user.type == "ADMIN":
            approved_notetakers = userRepository.get_users_by_account_type_and_approval("TAKER", True)
            unapproved_notetakers = userRepository.get_users_by_account_type_and_approval("TAKER", False)
            approved_noterequesters = userRepository.get_users_by_account_type_and_approval("REQUESTER", True)
            unapproved_noterequesters = userRepository.get_users_by_account_type_and_approval("REQUESTER", False)
            return render_template('admin-students.html', approved_notetakers=approved_notetakers, unapproved_notetakers=unapproved_notetakers, approved_noterequesters=approved_noterequesters,unapproved_noterequesters=unapproved_noterequesters, username = username, userType = user.type)
    return redirect(url_for('index'))

@app.route('/admin/approved_notetakers')
def approved_notetakers():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        if user.type == "ADMIN":
            approved_notetakers = userRepository.get_users_by_account_type_and_approval("TAKER", True)
            return render_template('admin-approved-notetakers.html', approved_notetakers=approved_notetakers, username = username, userType = user.type)
    return redirect(url_for('index'))

@app.route('/admin/unapproved_notetakers')
def unapproved_notetakers():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        if user.type:
            unapproved_notetakers = userRepository.get_users_by_account_type_and_approval("TAKER", False)
            return render_template('admin-unapproved-notetakers.html', unapproved_notetakers=unapproved_notetakers, username = username, userType = user.type)
    return redirect(url_for('index'))

@app.route('/admin/approved_noterequesters')
def approved_noterequestors():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        if user.type == "ADMIN":
            approved_noterequesters = userRepository.get_users_by_account_type_and_approval("REQUESTER", True)
            return render_template('admin-approved-noterequesters.html', approved_noterequesters=approved_noterequesters, username = username, userType = user.type)
    return redirect(url_for('index'))

@app.route('/admin/unapproved_noterequesters')
def unapproved_noterequesters():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        if user.type == "ADMIN":
            unapproved_noterequesters = userRepository.get_users_by_account_type_and_approval("REQUESTER", False)
            return render_template('admin-unapproved-noterequesters.html', unapproved_noterequesters=unapproved_noterequesters, username = username, userType = user.type)

@app.route('/admin/matches')
def get_matches():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        courseRepository = CourseRepository()
        user = userRepository.find(username)
        if user.type == "ADMIN":
            matchesRepository = MatchesRepository()
            matches = matchesRepository.get_matches()
            matches_list = []
            for match in matches:
                notetaker_id = match.notetaker_id
                notetaker = userRepository.find(notetaker_id)
                noterequester_id = match.noterequester_id
                noterequester = userRepository.find(noterequester_id)
                course_id = match.course_id
                course = courseRepository.find(course_id)
                match = (notetaker, noterequester, course)
                matches_list.append(match)
            return render_template('admin-matches.html', matches=matches, matches_list=matches_list, username = username, userType = user.type)
    return redirect(url_for('index'))

@app.route('/admin/matches_for_notetaker/<username>')
def matches_for_notetakers(username):
    if g.user:
        username = session['username']
        userRepository = UserRepository();
        user = userRepository.find(username)
        matchesRepository = MatchesRepository()
        matches = matchesRepository.get_matches_for_notetaker(username)
        return render_template('admin-view.html', users=matches, username = username, userType = user.type)
    return redirect(url_for('index'))

@app.route('/admin/matches_for_noterequester/<username>')
def matches_for_noterequesters(username):
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        matchesRepository = MatchesRepository()
        matches = matchesRepository.get_matches_for_noterequester(username)
        return render_template('admin-view.html', users=matches, username = username, userType = user.type)
    return redirect(url_for('index'))

@app.route('/admin/feedback')
def get_feedback():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        feedbackRepository = FeedbackRepository()
        feedback = feedbackRepository.get_feedback()
        return render_template('admin-feedback.html', users=feedback, username = username, userType = user.type)
    return redirect(url_for('index'))

@app.route('/admin/approve/<username>')
def approve(username):
    username = username
    userRepository = UserRepository()
    user = userRepository.find(username)
    user.approved = 1
    userRepository.save_changes()
    return render_template('admin-approval.html', user=user)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if g.user:
        username = session['username']
        userRepository = UserRepository()
        user = userRepository.find(username)
        form = FeedbackForm()
        if request.method == 'POST':
            if form.validate() == False:
                #flash('All fields are required')
                return render_template('feedback.html', form=form)
            else:
                msg = Message(form.subject.data, sender='gburdell369@gmail.com', recipients=['gburdell369@gmail.com'])
                msg.body = """
                From: %s <%s>
                %s
                """ % (form.name.data, form.email.data, form.message.data)
                mail.send(msg)
                #making a post to the table
                feedbackRepository = FeedbackRepository()
                username = session['username']
                feedback_text = form.message.data
                feedbackRepository.add_or_update(username, feedback_text)
                feedbackRepository.save_changes()

                return render_template('feedback.html', success=True, username = username, firstName = user.first_name, lastName = user.last_name, userType = user.type)
        elif request.method == 'GET':
            return render_template('feedback.html', form=form, username = username, firstName = user.first_name, lastName = user.last_name, userType = user.type)
    return redirect(url_for('index'))

api.add_resource(scribe_api.UserRegistration, '/api/register')
api.add_resource(scribe_api.UserLogin, '/api/login')
api.add_resource(scribe_api.HandleNotes, '/api/notes')
api.add_resource(scribe_api.CourseRegistration, '/api/course/register')
api.add_resource(scribe_api.CourseNumbersOnly, '/api/courses/distinct/<course_subject>')
api.add_resource(scribe_api.CourseSectionsOnly, '/api/courses/distinct/<course_subject>/<course_number>')
api.add_resource(scribe_api.CourseByCrn, '/api/courses/crn/<crn>')
api.add_resource(scribe_api.CourseNumbersBySubject, '/api/courses/<course_subject>') #not really used, but nice for testing
api.add_resource(scribe_api.CoursesSectionsByNumberSubject, '/api/courses/<course_subject>/<course_number>') #not really used, but nice for testing

