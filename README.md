# Senior Project

The project consists of an application that allows users to scan gym equipment using their phone camera and get a video demonstration on how to use the machine.

The application leverages AWS Rekognition's Custom Labels feature to identify gym equipment in user provided images. The returned labels are used to lookup excercises that can be performed using the identified machine in a SQLite database that is "shipped" with the app. 
The user is then presented with excercise choices for the muscle group they intend to work.

Video capture of running application: https://www.youtube.com/shorts/HY3wPQTl8oE?feature=share


## Repository contents:

### cv_service:
  -  A flask server that interfaces between clients and the AWS Rekognition API.

### dataset_builder
  - Python scripts used to simplify the process of building datasets.

### tests
  - Testing script for AWS Rekognition model. 

### client
  - An Android client built with Flutter.

### dataset
  - The dataset used to train AWS Rekognition Custom Labels. Built from online images with the help of dataset_builder tools.