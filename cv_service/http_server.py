# Provides an API for the front end to query Rekognition without storing its own credentials
# Need to replace or wrap with a production ready server like waitress

from flask import Flask, request
import boto3

app = Flask(__name__)


def get_label(img):
    model = ('arn:aws:rekognition:us-east-1:422292458603:project/gym_equipment/version/gym_equipment.2023-09-19T00.49'
             '.22/1695098962266')
    rekognition = boto3.client("rekognition", region_name='us-east-1')
    response = rekognition.detect_custom_labels(Image={'Bytes': img},
                                                MinConfidence=50,
                                                ProjectVersionArn=model)
    if len(response['CustomLabels']) > 0:
        # need to modify this to return the full label response to the client
        return response['CustomLabels'][0]['Name']
    else:
        return 'No Match'


@app.route('/label', methods=['POST'])
def label():
    return get_label(request.data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
