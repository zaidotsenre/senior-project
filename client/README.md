# Senior Project - Android Client

An Android client for my team's Senior Project in Information Technology. 
Users scan gym equipment using their phone camera and get a video demonstration on how to use the machine. 
Built with Flutter.


The application leverages AWS Rekognition's Custom Labels feature to identify gym equipment in user provided images. The returned labels are used to lookup excercises that can be performed using the identified machine in a SQLite database that is "shipped" with the app. The user is then presented with excercise choices to for the muscle group they intend to work. 


Video capture of running application: https://www.youtube.com/shorts/HY3wPQTl8oE?feature=share
