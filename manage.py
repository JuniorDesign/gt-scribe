#manages the db that we import from "scribe" package

import argparse
from scribe import db
from scribe.model.base import BaseModel
from scribe.model.user import User
#if you create a new model, import it here


#run this command everytime you create a new model
#python3 manage.py create_db
def create_db():
    db.create_all()

#run this command everytime you create a new model
#python3 manage.py drop_db
def drop_db():
    db.drop_all()


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