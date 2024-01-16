from flask import Flask, request
import requests
from joblib import load
import numpy as np
import json
from flask_sock import Sock
from PIL import Image
import boto3

import time  # only needed for testing

app = Flask(__name__)
app.debug = False
sock = Sock(app)


@app.route("/")
def home():
    return "<h1>Classification Server</h1>"


@sock.route("/echo")
def ws_process(ws):
    while True:
        data = ws.receive()
        ws.send("Classification Server is echoing: " + data)


# ['Planetscope Superdove', 'Orbital Megalaser', 'Global Gigablaster']
@sock.route("/ws-classify")
def ws_classify(ws):
    app.logger.debug("handling classification")
    data = ws.receive()
    classification_obj = create_classify_object(data)
    # # if request is invalid end connection
    if classification_obj is None:
        ws.send("REJECTED")
        return

    # retrieve ID from the JSON data, assuming it has field called 'classifier_id'
    classifier_id = classification_obj["classifier_id"]
    ws.send("ACCEPTED")
    np_array = np.array(classification_obj["image_data"]).reshape(
        classification_obj["shape"]
    )

    # filter image based on classifier_id
    np_array = filter_image(np_array, classifier_id)
    tinted_image = Image.fromarray(np_array.astype("uint8"), "RGB")
    tinted_image.save("tinted_image.png")

    # including id parameter
    # classification = classify(np_array, classifier_id)
    # app.logger.debug(classification)
    ws.send("DONE")
    ws.send((classification))
    ws.close(0)


def filter_image(np_array, id):
    if id == "Planetscope Superdove":
        return filter_planetscope(np_array)
    elif id == "Orbital Megalaser":
        return filter_orbital(np_array)
    elif id == "Global Gigablaster":
        return filter_global(np_array)
    else:
        return np_array


def filter_planetscope(np_array):
    # tint red
    np_array[:, :, 0] = np.clip(np_array[:, :, 0] + 50, 0, 255)
    return np_array


def filter_orbital(np_array):
    # tint blue
    np_array[:, :, 2] = np.clip(np_array[:, :, 2] + 50, 0, 255)
    return np_array


def filter_global(np_array):
    # tint green
    np_array[:, :, 1] = np.clip(np_array[:, :, 1] + 50, 0, 255)

    return np_array


# @sock.route('/ws-request-classifier')
# def ws_request_classifier(ws):
#     app.logger.debug("handling classifier request")
#     data = ws.receive()

#     # hypothetical function to get from json file
#     request_obj = create_request_object(data)

#     if request_obj is None:
#         ws.send("REJECTED")
#         return

#     classifier_id = request_obj['classifier_id']

#     # we can check if valid, but do we need when only dropdown to select possible options?
#     # if classifier_id not in available_classifier_ids:
#     #     ws.send("Invalid Classifier ID")
#     #     return

#     ws.send('ACCEPTED')
#     send_classifier_model(ws, classifier_id)
#     ws.close(0)


# validate that the incoming json has all the required fields
def create_classify_object(data):
    app.logger.warning("validating request: " + data)
    try:
        request_json = json.loads(data)
        if "classifier_id" not in request_json:
            app.logger.warning("no classifier_id")
            return None
        if "image_data" not in request_json:
            app.logger.warning("no image_data")
            return None
        return request_json
    except Exception as e:
        app.logger.error(e)
        return None


# classify the given array
# classifier_id is string name of (name)_classifier
def classify(array, classifier_id):
    # temporarily update progress bar
    # update_bar(uid=uid, progress=50)

    # flag is array doesn't line up with classifier throw error?
    # how to check that though

    # try if the classifier_id is actually a real joblib
    id = "res/{}.joblib".format(classifier_id)
    try:
        clf = load(id)
    except Exception as e:
        app.logger.error(e)
        return None

    app.logger.warning("joblib loaded")
    output = clf.predict(array)
    output = output.tolist()

    app.logger.warning("predicted on array")
    output_json = {"status": "DONE", "data": output}

    # return array of 1's and 0's
    return output


if __name__ == "__main__":
    s3 = boto3.client("s3")
    bucket_name = "plantify-test-bucket"
    object_key = "Classify.json"
    local_file_name = "Classify.json"
    s3.download_file(bucket_name, object_key, local_file_name)

    # print the first line of classify.json
    with open("Classify.json", "r") as f:
        print(f.readline())
        print(f.readline())
        print(f.readline())
        print(f.readline())

    app.run(debug=False, port=5001, host="0.0.0.0")
    # app.run(debug=True, port=5001)
