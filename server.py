from flask import Flask, request
import requests
from joblib import  load
import numpy as np
import json
from flask_sock import Sock
import time # only needed for testing

app = Flask(__name__)
app.debug = True
sock = Sock(app)

@app.route("/")
def home():
    return "<h1>Classification Server</h1>"

@sock.route('/echo')
def ws_process(ws):
    while(True):
        data = ws.receive()
        ws.send("Classification Server is echoing: " + data)

@sock.route('/ws-classify')
def ws_classify(ws):
    app.logger.debug("handling classification")
    data = ws.receive()
    classification_obj = create_classify_object(data)
    # # if request is invalid end connection
    if classification_obj is None:
        ws.send("REJECTED")
        return


    ws.send('ACCEPTED')
    np_array = np.array(classification_obj['image_data'])
    classification = classify(np_array)
    app.logger.debug(classification)
    ws.send('DONE')
    ws.send((classification))
    ws.close(0)


# validate that the incoming json has all the required fields
def create_classify_object(data):
    app.logger.warning("validating request: " + data)
    try:
        request_json = json.loads(data)
        if 'classifier_id' not in request_json:
            app.logger.warning("no classifier_id")
            return None
        if 'image_data' not in request_json:
            app.logger.warning("no image_data")
            return None
        return request_json
    except Exception as e:
        app.logger.error(e)
        return None


def classify(array):
    # future classification code

    # temporarily update progress bar
    # update_bar(uid=uid, progress=50)
     
    clf = load('res/ex_classifier.joblib')
    app.logger.warning("joblib loaded")
    output = clf.predict(array)
    output = output.tolist()

    app.logger.warning("predicted on array")
    output_json = {
        "status":"DONE",
        "data":output
        }

    # return array of 1's and 0's
    return output
  

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
    # app.run(debug=True, port=5001)