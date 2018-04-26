import requests
import json
import metaServer

payload = {'phrase': 'play California love'}
response = requests.post("http://127.0.0.1:5000", data=payload)
print(response.json())
metaServer.parse(response.json())


#curl --data "phrase=play California love" http://127.0.0.1:5000

