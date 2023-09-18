# A python script to assist in the creation of training and testing datasets
# for our custom AWS Rekognition Model
#

# Written by: Ernesto Diaz
# Senior Project in IT @ University of South Florida
# Group 12
# Fall 2023

# input:
#   a text file with a list of gym equipment names
#   the maximum number of images to be downloaded per equipment

# output:
#   an organized collection of images (no persons))

import os
import boto3
import cv2
import numpy as np
import bing_downloader


def get_image_from_file(filename):
    with open(filename, 'rb') as img_file:
        return img_file.read()


def remove_invalid_format(directory):
    for file in os.listdir(directory):
        if file.endswith(".jpg") or file.endswith(".png"):
            continue
        else:
            os.remove(directory + "/" + file)


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


def detect_humans(img):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    if img.shape[1] < 400:
        (height, width) = img.shape[:2]
        ratio = width / float(width)
        img = cv2.resize(img, (400, height * ratio))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return hog.detectMultiScale(img, winStride=(2, 2), padding=(10, 10), scale=1.02)


def remove_with_humans_cv2(directory, confidence=0.9):
    print('\n\n')
    print(f"Removing images with humans from {directory}...")
    for img_path in os.listdir(directory):
        print('\n\n')
        print(f'Checking {img_path}...')
        img_path = f'{directory}{img_path}'
        img = cv2.imread(img_path)
        (positions, weights) = detect_humans(img)
        for weight in weights:
            if weight >= confidence:
                os.remove(img_path)
                print(f"Removed {img_path}.")
                break


def remove_solid_bg(img_path):
    if os.path.exists(img_path):
        print(f'Looking for solid background in: {img_path}')
        try:
            img = cv2.imread(img_path)
            sections = [img[:, 0], img[:, -1], img[0, :], img[-1, :]]
            for section in sections:
                if (np.isclose(section, section[0, 0], rtol=0, atol=5).sum() / section.size) > 0.3:
                    os.remove(img_path)
                    return True
        except Exception as e:
            return False
    return False


