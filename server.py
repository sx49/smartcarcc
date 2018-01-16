#!flask/Scripts/python
"""
server module

When run as a script, this module will start the application and allow users to
retrieve information specified in the Smartcar API specification.
"""
from flask import Flask, jsonify, make_response, request
import requests
import json

app = Flask(__name__)       # Creates new application for script to run

# GET Vehicle Info
@app.route('/vehicles/<vid>', methods=['GET'])
def get_info(vid):
    # Retrieve information from GM API
    value = {"id": vid, "responseType": "JSON"}
    r = requests.post('http://gmapi.azurewebsites.net/getVehicleInfoService', json = value).json()

    # Extracts data from the request JSON
    result = {}
    data = ["vin","color","driveTrain"]
    for v in data:
        result[v] = r["data"][v]["value"]

    # Extracts door count data
    if (bool(r["data"]["fourDoorSedan"]["value"])):
        result["doorCount"] = 4
    elif (bool(r["data"]["twoDoorCoupe"]["value"])):
        result["doorCount"] = 2
    else:
        print "Error: no door count"

    # Didn't use ternary operator (shown below) in case there are more door types in the future
    # result["doorCount"] = 4 if bool(r["data"]["fourDoorSedan"]["value"]) else 2

    return jsonify(result)

# GET Security
@app.route('/vehicles/<vid>/doors', methods=['GET'])
def get_security(vid):
    # Retrieve information from GM API
    value = {"id": vid, "responseType": "JSON"}
    r = requests.post('http://gmapi.azurewebsites.net/getSecurityStatusService', json = value).json()

    # Extracts security info for each door
    result = []
    door_arr = r["data"]["doors"]["values"]
    for d in door_arr:
        data = {}
        data["location"] = d["location"]["value"]
        data["locked"] = bool(d["location"]["value"])
        result.append(data)

    return jsonify(result)

# GET Fuel Range
@app.route('/vehicles/<vid>/fuel', methods=['GET'])
def get_fuel(vid):
    # Retrieve information from GM API
    value = {"id": vid, "responseType": "JSON"}
    r = requests.post('http://gmapi.azurewebsites.net/getEnergyService', json = value).json()

    # Extracts fuel level
    # Null values are treated as empty [e.g. purely electric car has 0% fuel level])
    result = {}
    if (r["data"]["tankLevel"]["type"] == "Null"):
        result["percent"] = 0.0
    else:
        result["percent"] = float(r["data"]["tankLevel"]["value"])
    return jsonify(result)

# GET Battery Range
@app.route('/vehicles/<vid>/battery', methods=['GET'])
def get_battery(vid):
    # Retrieve information from GM API
    value = {"id": vid, "responseType": "JSON"}
    r = requests.post('http://gmapi.azurewebsites.net/getEnergyService', json = value).json()

    # Extracts battery level
    # Null values are treated as empty [e.g. purely fuel car has 0% battery level])
    result = {}
    if (r["data"]["batteryLevel"]["type"] == "Null"):
        result["percent"] = 0.0
    else:
        result["percent"] = float(r["data"]["batteryLevel"]["value"])
    return jsonify(result)

# POST Start/Stop Engine
@app.route('/vehicles/<vid>/engine', methods=['POST'])
def change_engine(vid):
    if not request.json:
        abort(400)

    # Retrieve information from GM API
    value = {"id": vid, "command": request.json["action"] + "_VEHICLE", "responseType": "JSON"}
    r = requests.post('http://gmapi.azurewebsites.net/actionEngineService', json = value).json()

    # Extracts outcome
    result = {}
    result["status"] = "success" if (r["actionResult"]["status"] == "EXECUTED") else "failure"

    return jsonify(result), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
