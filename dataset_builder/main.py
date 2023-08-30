from bing_image_downloader import downloader
import cv2
import os

human_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')


def detect_people(img_path):
    image = cv2.imread(img_path)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # detect humans in input image
    (humans, _) = hog.detectMultiScale(image, winStride=(10, 10),
                                       padding=(32, 32), scale=1.1)

    # getting no. of human detected
    print('Human Detected : ', len(humans))
    print(humans)
    if len(humans) > 0:
        return True
    else:
        return False


def get_img_paths(directory):
    return [path for path in os.listdir(directory) if path.endswith(".jpg") or path.endswith(".png")]


for path in get_img_paths("dataset/back extension"):
    if detect_people("dataset/back extension/" + path):
        os.remove("dataset/back extension/" + path)
        print("Removed dataset/back extension/" + path)


# queries = {"leg press", "back extension"}
# for query in queries:
#    downloader.download(query, limit=100, output_dir='dataset',
#                        adult_filter_off=True, force_replace=False, timeout=60)

