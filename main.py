#Importing required libraries
from flask import Flask, jsonify, render_template, request
import datetime
from datetime import datetime as dt
import cowinApp

app = Flask(__name__)

#Functions check for the appointment availablity using the COWIN API and cowinApp.py
@app.route('/checkAvailablity')
def checkAppointementAvailablity():
    #Store the input from user else use the default value
    pincodeFromUser = request.args.get('inputPincode', 100000, type=int)
    ageFromUser = request.args.get('inputAge', 18, type=int)
    dateFromUser = request.args.get('weekChange', 0, type=int)
    currentDate = dt.now() + datetime.timedelta(7*dateFromUser)
    
    #Call the checkAppointmentAvailability function from cowinApp.py to GET information from API and have the output
    status = cowinApp.checkAppointmentAvailability(pincodeFromUser,currentDate,ageFromUser,0)

    #Returing the return the checkAppointmentAvailability function
    return status

#Running the main flask app on index.html
@app.route('/')
def index():
    return render_template('index.html')
