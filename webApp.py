import urllib
import json
import os
import requests

from datetime import datetime
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/mausam', methods=['POST'])

def mausam():
    req = request.get_json(silent=True)
    result = req.get("queryResult")
    txt = result.get("queryText")
    para = result.get("parameters")
    ser = para.get("weather")
    
    res = getData(ser, txt)
    
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
 
def getData(ser, txt):
    url = "https://api.openweathermap.org/data/2.5/onecall"

    headers = {
        'lat': "12.9716",
        'lon': "77.5946",
        'exclude':"current, minutely, daily",
        'appid':"55d9b247cd8975310c07f8e2230cade4"
        }

    #make connection and get response
    response = requests.request("GET", url, params=headers)
    hourly = response.json()['hourly']
    
    found = 0
    date = 0
    des = ''
    

    for h in hourly:
        if (h['weather'][0]['main'] == ser):
            found = 1
            date = h['dt']
            des = h['weather'][0]['description']
            break

        
    return respond(txt, des, date, found)

def respond(txt, des, date, found):

    date = datetime.fromtimestamp(date).strftime('%H%M')
    if found == 0 :
        ans = "No forcast for " + txt + " in next 24 hours. Plesae ask about other conditions."
    elif found == 1 :
        time = datetime.now().strftime('%H%M')
        time = int((int(date) - int(time))/100)
        ans = "There are some chances of " + des + " starting in next " + str(time) + " hours"
    
    res = {        
        "displayText": ans,
        "fulfillmentText": ans,
        #"data": {},
        #"contextOut": [],
        "source": "Mausam"
    }
    
    return res
    
