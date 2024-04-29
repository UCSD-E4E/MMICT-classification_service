import requests
import json

# Define the endpoint URL
url = 'http://127.0.0.1:5001/classification-service/classify'

# Define the data to be sent in the request body
data = {
    'image': [1, 2, 3, 4, 5],
    'uid': 12345
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Define the headers for the request
headers = {
    'Content-Type': 'application/json'
}

# Send the POST request with the JSON data and headers
response = requests.post(url, data=json_data, headers=headers)

# Print the response
print(response.content)
