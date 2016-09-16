from flask import Flask, render_template
from flask_restful import Api
#import api as restapi
#api.py was another file that contained the class resources below


app = Flask(__name__)
app.debug = True
api = Api(app)


@app.route('/')
def index():
	return render_template("index.html")

#example set up from my last project
#api.add_resource(restapi.LoginResource, '/api/login')
#api.add_resource(restapi.ReservationResource, '/api/reservation/<string:reservation_id>') #includes update_reservation
#api.add_resource(restapi.UpdateReservationConfirmResource, '/api/reservation/<string:reservation_id>/availability')


if __name__ == '__main__':
	app.run('0.0.0.0', 5000, debug=True)


