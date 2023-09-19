import os
import hashlib
import imagehash
from PIL import Image


def main2():
    img_hashes = set()
    for path in os.listdir():
        f = open(path, 'rb')
        img = f.read()
        f.close()
        img_hash = hashlib.md5(img).hexdigest()
        if img_hash in img_hashes:
            os.remove(path)
        else:
            img_hashes.add(img_hash)


def has_near_duplicate(img_hashes, img_hash, tolerance):
    for h in img_hashes:
        if abs(h - img_hash) <= tolerance:
            return True


def main():
    img_hashes = set()
    for path in os.listdir():
        img = Image.open(path).convert('RGBA')
        img_hash = imagehash.average_hash(img)
        if has_near_duplicate(img_hashes, img_hash, 10):
            os.remove(path)
        else:
            img_hashes.add(img_hash)


if __name__ == '__main__':
    main()
