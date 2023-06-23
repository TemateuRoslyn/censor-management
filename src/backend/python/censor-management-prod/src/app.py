# app.py
from flask import Flask, jsonify, request
import json,time


# models
from accelerometre1 import Accelerometre1

app = Flask(__name__)

acc1 =  Accelerometre1()


@app.route('/', methods=['GET'])
def index():
    return 'welcome to our website'

@app.route('/accelerometre/insert', methods=['GET'])
def store_data():
    if acc1.set_next():
        return 'Insert successfully !'
    else :
        return 'An error occur !'

@app.route('/accelerometre1/next', methods=['GET'])
def get_employees():
    nextCapteurValue = acc1.get_next()
    return json.dumps(nextCapteurValue)


if __name__ == '__main__':
    app.run(port=8000)

