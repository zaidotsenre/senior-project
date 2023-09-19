from flask import Flask, request
import boto3

app = Flask(__name__)

def get_labels(img):
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_labels(Image={'Bytes': img},
                                         Settings={"GeneralLabels": {"LabelInclusionFilters": ["Person"]}})
    for label in response["Labels"]:
        if label["Name"] == "Person":
            os.remove(path)

@app.route('/label', methods=['POST'])
def label():
    with open('output.png', 'wb') as img:
        img.write(request.data)
    return 'Received !'  # response to your request.



