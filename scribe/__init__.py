#initializes the application
#creates the "scribe" package, so now we can import variables from "scribe"
#(any folder with an __init__.py can be imported as a package)
#creates a new instance of flask, creates a new instance of the db
import json

from flask import Flask, render_template
from flask.sessions import SecureCookieSession, SecureCookieSessionInterface
from flask_restful import Api
import flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/temp.db'

class JSONSecureCookieSession(SecureCookieSession):
    serialization_method = json

class JSONSecureCookieSessionInterface(SecureCookieSessionInterface):
    session_class = JSONSecureCookieSession

app.secret_key = 'foobar'
app.session_interface = JSONSecureCookieSessionInterface()

S3_LOCATION = 'http://gt-scribe.s3.amazonaws.com'
S3_KEY = 'key'
S3_SECRET = 'secret_key'
S3_UPLOAD_DIRECTORY = ''
S3_BUCKET = 'gt-scribe'

db = SQLAlchemy(app)

import scribe.routes

