from flask import Flask, render_template, request
from flask_restful import Api
#import api as restapi
#api.py was another file that contained the class resources below


app = Flask(__name__, static_url_path='')
app.debug = True
api = Api(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/requester')
def requester():
	return render_template('requester.html')

@app.route('/taker')
def taker():
	return render_template('taker.html')

#example set up from my last project
#api.add_resource(restapi.LoginResource, '/api/login')
#api.add_resource(restapi.ReservationResource, '/api/reservation/<string:reservation_id>') #includes update_reservation
#api.add_resource(restapi.UpdateReservationConfirmResource, '/api/reservation/<string:reservation_id>/availability')


if __name__ == '__main__':
	app.run('0.0.0.0', 5000, debug=True)


