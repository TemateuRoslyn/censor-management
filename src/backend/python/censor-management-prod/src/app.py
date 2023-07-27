# app.py
import os
import json, time
from flask import Flask, jsonify, request

# Lire la valeur des variables d'environnement
debug_val = os.getenv("debug")  # La variable "debug" sera soit True ou False (str)
host_val = os.getenv("host")    # La variable "host" contiendra l'adresse (str)
port_val = os.getenv("port")    # La variable "port" contiendra le port (str)


# Convertir le port en nombre (integer)
try:
    port_val = int(port_val)
except ValueError:
    print("Erreur : le port n'est pas un entier valide.")
    
if debug_val == "true":
    debug_val = True
else:
    debug_val = False


# models
from accelerometre_rand import Accelerometre1
from accelerometre2 import Accelerometre2
from tracking import Tracker
from analogic_input import AnalogicInput

app = Flask(__name__)

acc1 = Accelerometre1()
acc2 = Accelerometre2()
tr = Tracker()
ai = AnalogicInput()


@app.route("/", methods=["GET"])
def index():
    return "welcome to our website"


@app.route("/accelerometre/insert", methods=["GET"])
def store_data():
    if acc1.set_next():
        return "Insert successfully !"
    else:
        return "An error occur !"


@app.route(
    "/analogic-input",
    methods=["GET"],
)
def get_ai():
    result = ai.get_value()
    return json.dumps(result)


@app.route(
    "/accelerometre/next",
    methods=["GET"],
)
def get_employees():
    cycle = 5
    if request.args.get("cycle") is not None:
        cycle = request.args.get("cycle")
    nextCapteurValue = acc1.get_next(float(cycle))
    return json.dumps(nextCapteurValue)


@app.route("/acc2/next", methods=["GET"])
def get_accelerometre2():
    nextCapteurValue = acc2.get_next()
    return json.dumps(nextCapteurValue)


@app.route("/tracking/insert", methods=["GET"])
def store_position():
    city = request.args.get("city")
    state = request.args.get("state")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if tr.set_next(city, state, lat, lon):
        return "Insert successfully !"
    else:
        return "An error occur !"


@app.route(
    "/tracking/next",
    methods=["GET"],
)
def coordinates():
    nextCapteurValue = tr.get_next()
    return json.dumps(nextCapteurValue)


if __name__ == "__main__":
    app.run(
        debug=debug_val, true
        host=host_val,
        port=port_val, 
        )
