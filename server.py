from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Classification Server</h1>"

@app.route("/classification-service/classify", methods=['POST'])
def classify_route():
    # parse for the processed image
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        # example of how parsing data should look
        json['example'] = 'new data'
        image = json['image']
        uid = json['uid']
        data = classify(image,uid)
        return data
    else:
        return 'Content-Type not supported!'

def classify(array, uid):
    # future classification code

    # temporarily update progress bar
    update_bar(uid=uid, progress=50)

    # return array of 1's and 0's
    return array

def update_bar(uid, progress):
    payload = {'uid':uid, 'progress':progress}
    r = requests.get('http://main-server/progress',params=payload)
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)