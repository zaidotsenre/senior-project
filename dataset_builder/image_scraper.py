# A simple script intended to scrape images off Google image search results
# Input: a url
# Output: A folder containing the downloaded images.

import re
import sys

import requests


def download(url):
    # send request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/117.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        print(f'Downloading images from {url}')

        #look for links in the response
        pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
        links = re.findall(pattern, response.text)

        # make new list with only links to images
        img_links = []
        for link in links:
            if re.search('\.(jpg|png|jpeg)\Z', link) is not None:
                img_links.append(link)

        # download images
        for i, link in enumerate(img_links):
            response = requests.get(link, headers=headers)
            img = response.content
            img_ext = link.rsplit('.', 1)[-1]
            img_name = f'Image_{i}.{img_ext}'
            with open(img_name, 'wb') as f:
                f.write(img)
    else:
        print('Sorry, unable to fetch the data from the server.')


def main():
    url = sys.argv[1]
    download(url)


if __name__ == '__main__':
    main()