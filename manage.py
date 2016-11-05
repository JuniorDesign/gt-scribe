#manages the db that we import from "scribe" package

import argparse
import json
from scribe import db
from scribe.model.base import BaseModel
from scribe.model.user import User
from scribe.model.course import Course
from scribe.model.file import File 
from scribe.model.enrollment import Enrollment
from scribe.model.matches import Matches
from scribe.model.feedback import Feedback
from scribe.repositories.courseRepository import CourseRepository
from scribe.repositories.userRepository import UserRepository
#if you create a new model, import it here


#run this command everytime you create a new model
#python3 manage.py create_db
def create_db():
    db.create_all()

#run this command everytime you create a new model
#python3 manage.py drop_db
def drop_db():
    db.drop_all()

#called in create_db, fills the db with fall 2016 courses
def populate_courses():
    try:
        with open('courses.json') as courses_json:
            courses = json.loads(courses_json.read())
        courseRepository = CourseRepository()
        for course in courses:
            if 'sections' in course: #courses without this aren't actually offered, they lack section number and crn
                for section in course['sections']:
                    subject = course['school'] #CS, MATH, etc
                    if 'number' in course:
                        course_number = course['number'] #1331, 1332, etc
                    else: #we should never hit this with the above checks, but just in case
                        course_number = '0000'
                    section_id = section['section_id']
                    crn = section['crn'] 
                    newCourse = Course(crn, subject, course_number, section_id, crn)
                    #lets consider dropping the course_id and only using crn, since crns are unique
                    courseRepository.add_or_update(newCourse)
        courseRepository.save_changes()
        print("Courses have been successfully added!")
    except Exception as e:
        print("The database has likely already been populated with courses.")
        print("---------------------------------------------------------")
        print(e)

#makes default user accounts, called in create_db
def populate_users():
    try:
        userRepository = UserRepository()
        newAdmin = User('admin', '123', "gburdell@gatech.edu", 'First Name', 'Last Name', 'ADMIN', True)
        userRepository.add_or_update(newAdmin)
        userRepository.save_changes()
        print("All preset users added into database!")
    except:
        print("The database has already been populated with the preset users.")

        

def main():
    parser = argparse.ArgumentParser(
        description='Manage this Flask application.')
    parser.add_argument(
        'command', help='the name of the command you want to run')
    parser.add_argument(
        '--seedfile', help='the file with data for seeding the database')
    args = parser.parse_args()

    if args.command == 'create_db':
        create_db()
        print("Database has been created!")

    elif args.command == 'drop_db':
        drop_db()
        print("Database has been dropped and deleted!")

    elif args.command == 'populate_courses':
        populate_courses()    

    elif args.command == 'populate_users':
        populate_users()
        
    else:
        raise Exception('Invalid command')

if __name__ == '__main__':
    main()