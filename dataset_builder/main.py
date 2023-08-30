from bing_image_downloader import downloader
import cv2

human_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')


def detect_people(img_path):
    img = cv2.imread(img_path)
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    humans = human_casc


queries = {"leg press", "back extension"}
for query in queries:
    downloader.download(query, limit=100, output_dir='dataset',
                        adult_filter_off=True, force_replace=False, timeout=60)
