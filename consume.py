import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "Inputs": {
    "data": [
        {
        "instant" : 1,
        "date": "2011-01-01T00:00:00.000Z",
        "season" : 1,
        "yr" : 0,
        "mnth" : 1,
        "weekday" : 6,
        "weathersit" : 2,
        "temp" : 0.344167,
        "atemp" : 0.363625,
        "hum" : 0.805833,
        "windspeed" : 0.160446,
        "casual" : 331,
        "registered" : 654
        },
        {
        "instant" : 2,
        "date": "2011-02-01T00:00:00.000Z",
        "season" : 1,
        "yr" : 0,
        "mnth" : 1,
        "weekday" : 6,
        "weathersit" : 2,
        "temp" : 0.363478,
        "atemp" : 0.353739,
        "hum" : 0.696087,
        "windspeed" : 0.248539,
        "casual" : 131,
        "registered" : 670
        },
    ]
  },
  "GlobalParameters": {
    "method": "predict"
  }
}

input_data = json.dumps(data)
with open("data.json", "w") as _f:
    _f.write(input_data)

body = str.encode(json.dumps(data))

url = 'http://4832a788-2aa9-4c44-9def-0191f18bb88c.francecentral.azurecontainer.io/score'
api_key = 'KxgcNGo9oVmfZhYFyFyeSU506jjBdiQL' # Replace this with the API key for the web service

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))