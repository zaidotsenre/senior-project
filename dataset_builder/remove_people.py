import boto3


def remove_with_people(img_path, min_confidence=50):
    if os.path.exists(img_path):
        print(f'Looking for people in: {img_path}')
        rekognition = boto3.client("rekognition")
        img_bytes = get_image_from_file(img_path)
        try:
            response = rekognition.detect_labels(Image={'Bytes': img_bytes}, MinConfidence=min_confidence,
                                             Settings={"GeneralLabels": {"LabelInclusionFilters": ["Person"]}})
        except Exception as e:
            return False
        for label in response["Labels"]:
            if label["Name"] == "Person":
                os.remove(img_path)
                return True

    return False