import requests
import json
import metaServer

payload = {'phrase': 'please listen la brute a test'}
response = requests.post("http://127.0.0.1:5000", data=payload)
jsondata = response.json()
print(jsondata)
print(jsondata["song"])

#curl --data "phrase=play California love" http://127.0.0.1:5000

