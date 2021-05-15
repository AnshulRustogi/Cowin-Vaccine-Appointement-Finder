from flask import Flask, jsonify, render_template, request
import datetime
from datetime import datetime as dt
import cowinApp

app = Flask(__name__)

@app.route('/checkAvailablity')
def checkAppointementAvailablity():
    pincodeFromUser = request.args.get('inputPincode', 100000, type=int)
    ageFromUser = request.args.get('inputAge', 18, type=int)
    dateFromUser = request.args.get('weekChange', 0, type=int)
    currentDate = dt.now() + datetime.timedelta(7*dateFromUser)
    status = cowin.checkAppointmentAvailability(pincodeFromUser,currentDate,ageFromUser,0)
    #print(status)
    return status
    #return jsonify(result=a + b)

@app.route('/')
def index():
    return render_template('index.html')
