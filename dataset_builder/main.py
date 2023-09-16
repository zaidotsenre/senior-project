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

from bing_image_downloader import downloader
import os
import boto3
import cv2
import numpy as np


def get_image_from_file(filename):
    with open(filename, 'rb') as img_file:
        return img_file.read()


def remove_invalid_format(directory):
    for file in os.listdir(directory):
        if file.endswith(".jpg") or file.endswith(".png"):
            continue
        else:
            os.remove(directory + "/" + file)


def remove_with_people(directory, min_confidence=50):
    rekognition = boto3.client("rekognition")

    print('\n\n')
    print(f"Removing images with humans from {directory}...")
    for image in os.listdir(directory):
        print('\n\n')
        print(f'Checking {image}...')
        image = f'{directory}{image}'
        bytes = get_image_from_file(image)
        response = rekognition.detect_labels(Image={'Bytes': bytes}, MinConfidence=min_confidence,
                                             Settings={"GeneralLabels": {"LabelInclusionFilters": ["Person"]}})
        for label in response["Labels"]:
            if label["Name"] == "Person":
                os.remove(image)
                print(f"Removed {image}.")


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


def remove_solid_bg(directory):
    for file in os.listdir(directory):
        print(f'Removing white background images from: {directory}/{file}')
        img = cv2.imread(f'{directory}/{file}')
        sections = [img[:, 0], img[:, -1], img[0, :], img[-1, :]]
        for section in sections:
            if (np.isclose(section, section[0, 0], rtol=0, atol=5).sum() / section.size) > 0.3:
                os.remove(f'{directory}/{file}')
                break


if __name__ == "__main__":

    directory = "dataset"

    # get user input
    name = input("Enter name of equipment:")
    num_images = int(input("Number of images to download (per equipment):"))

    # download images
    downloader.download(name, limit=num_images, output_dir=directory,
                        adult_filter_off=True, force_replace=False, timeout=1)

    # delete images that are not .jpg or .png
    remove_invalid_format(f'{directory}/{name}/')

    # delete images with solid color backgrounds
    remove_solid_bg(f'{directory}/{name}/')

    # detect and delete images that contain humans
    remove_with_people(f'{directory}/{name}/')

    # rename remaining images
    num = 0
    for image in os.listdir(f'{directory}/{name}/'):
        image = f'{directory}/{name}/{image}'
        ext = image[image.find('.'):]
        os.rename(image, f'{directory}/{name}/{name.replace(" ", "_")}_{num}{ext}')
        num += 1
