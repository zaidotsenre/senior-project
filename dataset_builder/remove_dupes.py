import os
import hashlib


def main():
    for path in os.listdir():
        img_hashes = set()

        with open(path, "rb") as f:
            img = f.read()
            img_hash = hashlib.md5(img).hexdigest()
            if img_hash in img_hashes:
                os.remove(path)
            else:
                img_hashes.add(img_hash)
