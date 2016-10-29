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
from scribe.repositories.courseRepository import CourseRepository
#if you create a new model, import it here


#run this command everytime you create a new model
#python3 manage.py create_db
def create_db():
    db.create_all()
    populate_courses()

#run this command everytime you create a new model
#python3 manage.py drop_db
def drop_db():
    db.drop_all()

def populate_courses():
    with open('courses.json') as courses_json:
        courses = json.loads(courses_json.read())

    courseRepository = CourseRepository()
    counter = 0
    for course in courses: #each course object is now a json object for a course
        counter+=1 #used for our fake crn for testing, ensures unique primary keys
        print(course['name'])
        subject = course['school'] #CS, MATH, etc
        print("This is course subject: "+subject)
        if 'number' in course:
            course_number = course['number'] #1331, 1332, etc
        else:
            course_number = '0000' #Some weird courses are missing numbers but still in catalog, so just use this as a placeholder
        print("This is course number: "+course_number)
        section = 'A' #sections are stored inconveniently, so for testing real quick, just use this
        crn = str(counter)+subject+course_number+section #crn is located inside the sections array, so use this for quick testing
        print("This is course crn that I made up: "+crn)
        newCourse = Course(crn, subject, course_number, section, crn)
        courseRepository.add_or_update(newCourse)
    
    courseRepository.save_changes()
        

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
        
    else:
        raise Exception('Invalid command')

if __name__ == '__main__':
    main()