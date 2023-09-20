import requests
import json
import base64

with open('tst.jpeg', 'rb') as f:
    img = f.read()
    #r = requests.post("http://54.89.243.235:5000/label", data=img)
    r = requests.post("http://127.0.0.1:5000/label", data=img)

# And done.
print(r.text) # displays the result body.