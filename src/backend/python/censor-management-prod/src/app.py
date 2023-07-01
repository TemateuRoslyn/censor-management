# app.py
from flask import Flask, jsonify, request
import json, time


# models
from accelerometre_rand import Accelerometre1
from accelerometre2 import Accelerometre2
from tracking import Tracker

app = Flask(__name__)

acc1 = Accelerometre1()
acc2 = Accelerometre2()
tr = Tracker()


@app.route("/", methods=["GET"])
def index():
    return "welcome to our website"


@app.route('/tracking/insert', methods=['GET'])
def store_position():
    city = request.args.get('city')
    state = request.args.get('state')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if tr.set_next(city, state, lat, lon):
        return 'Insert successfully !'
    else :
        return 'An error occur !'


@app.route('/tracking/next', methods=['GET'],)
def coordinates():
    nextCapteurValue = tr.get_next()
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
    app.run(port=8000, debug=True)
