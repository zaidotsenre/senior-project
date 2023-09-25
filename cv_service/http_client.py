# This client is for testing purposes only.
# It will not be used in the application.

import requests

with open('tst.jpg', 'rb') as f:
    img = f.read()
    r = requests.post("http://54.89.243.235:5000/label", data=img)
    #r = requests.post("http://127.0.0.1:5000/label", data=img)
    print(r.text)