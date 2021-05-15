import requests
import json
import pandas as pd
import datetime
from datetime import date, datetime as dt, timedelta

currentDate = dt.now()
def createCalender(dateFromUserUnformated):
    calender = dict()
    for i in range(7):
        calender[i]=str((dateFromUserUnformated + datetime.timedelta(i)).strftime("%d-%m-%Y"))
    return calender

def formProperStructure(pincodeFromUser, jsonStructure, ageFromUser, currentDateList, check):
    #print(jsonStructure)
    if(len(jsonStructure['centers'])!=0):
        datasetList = jsonStructure['centers'][0]
                
        dataset = [] #Contains the list of all the headers
        for columnName in datasetList:
            dataset.append(columnName)
                
        testStructure = pd.DataFrame(jsonStructure['centers'],columns = dataset)
        testStructure = testStructure.drop(['lat', 'long', 'to', 'from', 'pincode', 'fee_type'], axis=1)
        testStructure = testStructure.set_index('center_id')
                
        for index,currentRow in testStructure.iterrows():
            number = 0
            iterations = len(currentRow['sessions'])
            while number < iterations:
                if currentRow['sessions'][number]['min_age_limit'] != ageFromUser or currentRow['sessions'][number]['available_capacity']==0:
                #if currentRow['sessions'][number]['min_age_limit'] != ageFromUser:
                    del currentRow['sessions'][number]
                    iterations -= 1
                else:
                    number += 1
                
        for index,currentRow in testStructure.iterrows():
            if len(currentRow['sessions']) == 0:
                testStructure = testStructure.drop(index)
                
        if(len(testStructure)==0):
            temp = datetime.date(int(currentDateList[0][6:10]),int(currentDateList[0][3:5]),int(currentDateList[0][0:2]))-datetime.timedelta(16)
            #return output + "<br>Sorry No appointements are avaiable in your pincode for this period. Please try again later"
            output = '<div class="timePeriod"><ul><li class="prev"><button onclick="previousWeek()">&#10094;</button></li><li class="next"><button onclick="nextWeek()">&#10095;</button></li>'
            output +=  '<li>Time Period: ' + temp.strftime("%d-%m-%y") + '&#10094;-&#10095;' + (temp+timedelta(23)).strftime("%d-%m-%y") + '<br></li></ul></div>'
            output += '<ul class="weekCalender"><li></li>'
            #for i in currentDateList:
            #    output += '<li>' + str(currentDateList[i]) +'</li>'
            #output += '</ul>'
    
            if(check>=3):
                return output + "<center>No appointement Avaiable in your region for the next 3 weeks</center>"
            return checkAppointmentAvailability(pincodeFromUser,datetime.date(int(currentDateList[0][6:10]),int(currentDateList[0][3:5]),int(currentDateList[0][0:2]))+datetime.timedelta(8),ageFromUser, check+1)

    else:
        output = '<div class="timePeriod"><ul><li class="prev"><button onclick="previousWeek()">&#10094;</button></li><li class="next"><button onclick="nextWeek()">&#10095;</button></li>'
        output +=  '<li>Time Period: ' + str(currentDateList[0]) + '&#10094;-&#10095;' + str(currentDateList[6]) + '<br></li></ul></div>'
        output += '<ul class="weekCalender"><li></li>'
        for i in currentDateList:
            output += '<li>' + str(currentDateList[i]) +'</li>'
        output += '</ul>'
        return output + "<br>Sorry No appointements are avaiable in your pincode for this period. Please try again later"
    
    output = '<div class="timePeriod"><ul><li class="prev"><button onclick="previousWeek()">&#10094;</button></li><li class="next"><button onclick="nextWeek()">&#10095;</button></li>'
    output +=  '<li>Time Period: ' + str(currentDateList[0]) + '&#10094;-&#10095;' + str(currentDateList[6]) + '<br></li></ul></div>'
    output += '<ul class="weekCalender"><li></li>'
    for i in currentDateList:
        output += '<li>' + str(currentDateList[i]) +'</li>'
    output += '</ul>'
    finalStructure = dict()
    for index,currentRow in testStructure.iterrows():
        temp = list()
        number = 0
        i = 0
        currentDate = datetime.date(2021,5,16)
        while number < 7:
            sessionAvaiable = list()
            sessionAvaiable.append(currentDate.strftime("%d-%m-%y"))
            lenght = len(currentRow['sessions'])
            if i < lenght and currentRow['sessions'][i]['date']==currentDateList[number]:
                sessionAvaiable.append(currentRow['sessions'][i]['available_capacity'])
                sessionAvaiable.append(currentRow['sessions'][i]['vaccine'])
                i+=1
                #print("Appointement available on",currentDate.strftime("%d-%m-%y"))
            else:
                sessionAvaiable.append("NO SLOT")
                sessionAvaiable.append("")
                #print("No appointement on",currentDate.strftime("%d-%m-%y"))
            temp.append(sessionAvaiable)
            currentDate += datetime.timedelta(1)
            number += 1
        finalStructure[currentRow['name']] = temp

    for currentCenter in finalStructure:
        output += '<ul class="days"><li>' + str(currentCenter) + '</li>'
        for sessions in finalStructure[currentCenter]:
            if sessions[1]=="NO SLOT":
                output +="<li>NO SLOT</li>"
            else:
                output +="<li>"+ str(sessions[1]) + ", "+ str(sessions[2]) + "</li>"
            
    output += '</ul>'
    #return json.dumps(finalStructure)
    return output

def checkFutureAppointment(pincodeFromUser: int, dateFromUserUnformated: str, ageFromUser: int):
    #print(pincodeFromUser, dateFromUser, ageFromUser)
    iterations = 0
    currentSearchDate = dateFromUserUnformated + datetime.timedelta(days=8)
    checkRequest = checkAppointmentAvailability(pincodeFromUser, currentSearchDate, ageFromUser)
    temp = checkRequest
    while iterations<=4:
        iterations += 1
        currentSearchDate = currentSearchDate+datetime.timedelta(days=8)
        checkRequest = checkAppointmentAvailability(pincodeFromUser, currentSearchDate, ageFromUser)        
    return

def checkAppointmentAvailability(pincodeFromUser: int, dateFromUserUnformated: datetime.datetime, ageFromUser: int, check):
    response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}".format(pincode = pincodeFromUser,date = dateFromUserUnformated.strftime("%d-%m-%Y")),headers={'User-Agent':'Chrome/88.0.4324.182'})
    #dateFromUserUnformated = datetime.date(2021,5,18)
    
    if(response.status_code==200):
        jsonStructure = response.json()
        print("Request Succesful with data: ",pincodeFromUser,dateFromUserUnformated,ageFromUser)
        if check!=0:
            return formProperStructure(pincodeFromUser, jsonStructure, ageFromUser, createCalender(dateFromUserUnformated),check+1)   
        else:
            return formProperStructure(pincodeFromUser, jsonStructure, ageFromUser, createCalender(dateFromUserUnformated),0)   
    else:
        print("Error Code: " + str(response.status_code))
        return "<script>alert{'SOME ERROR OCCURED! Please try again later'};</script>"

