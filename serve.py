#launches our local server on port 5000
#all routing info has been moved to route.py in the scribe folder

from flask import Flask, render_template, request
from flask_restful import Api

from scribe import app

if __name__ == '__main__':
	app.run('0.0.0.0', 5000, debug=True)


