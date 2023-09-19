import boto3
import os
import re


def get_image_from_file(path):
    with open(path, 'rb') as img_file:
        return img_file.read()


def main():
    for path in os.listdir():
        if re.search('\.(jpg|png|jpeg)\Z', path) is not None:
            img_bytes = get_image_from_file(path)
            rekognition = boto3.client("rekognition")
            response = rekognition.detect_labels(Image={'Bytes': img_bytes}, MinConfidence=70,
                                                 Settings={"GeneralLabels": {"LabelInclusionFilters": ["Person"]}})
            for label in response["Labels"]:
                if label["Name"] == "Person":
                    os.remove(path)


if __name__ == '__main__':
    main()
