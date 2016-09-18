#initializes the application
#creates the "scribe" package, so now we can import variables from "scribe"
#(any folder with an __init__.py can be imported as a package)
#creates a new instance of flask, creates a new instance of the db

from flask import Flask, render_template
from flask_restful import Api
import flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/temp.db'

db = SQLAlchemy(app)

import scribe.routes