# Deletes images in the current directory that have solid backgrounds

import numpy as np
import cv2
import os
import re


# input: img nparray
# output: true if img has solid background
def has_solid_bg(img):
    sections = [img[:, 0], img[:, -1], img[0, :], img[-1, :]]
    for section in sections:
        if (np.isclose(section, section[0, 0], rtol=0, atol=5).sum() / section.size) > 0.3:
            return True
    return False


def main():
    for path in os.listdir():
        if re.search('\.(jpg|png|jpeg)\Z', path) is not None:
            try:
                img = cv2.imread(path)
                if has_solid_bg(img):
                    os.remove(path)
            except Exception as e:
                continue


if __name__ == '__main__':
    main()
