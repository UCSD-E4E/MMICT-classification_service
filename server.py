from flask import Flask, request
import requests
from joblib import  load
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Classification Server</h1>"

@app.route("/classification-service/classify", methods=['POST'])
def classify_route():
    # parse for the processed image
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        request_data = request.json
        image = request_data['image']
        uid = request_data['uid']
        data = classify(image,uid)
        return json.dumps(data)
    else:
        return 'Content-Type not supported!'

def classify(array, uid):
    # future classification code

    # temporarily update progress bar
    # update_bar(uid=uid, progress=50)
     
    clf = load('res/ex_classifier.joblib')
    output = clf.predict(array)

    output = {
        'data':output
        }

    # return array of 1's and 0's
    return output

def update_bar(uid, progress):
    payload = {'uid':uid, 'progress':progress}
    _ = requests.get('http://main-server/progress',params=payload)
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)