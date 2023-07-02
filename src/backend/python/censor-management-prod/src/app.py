# app.py
from flask import Flask, jsonify, request
import json, time


# models
from accelerometre_rand import Accelerometre1
from accelerometre2 import Accelerometre2

app = Flask(__name__)

acc1 = Accelerometre1()
acc2 = Accelerometre2()


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


if __name__ == "__main__":
    app.run(port=8000, debug=True)
