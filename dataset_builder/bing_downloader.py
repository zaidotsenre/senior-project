import urllib
import urllib.request
import posixpath
import re
import pathlib


class BingDownloader:
    def __init__(self, query, out_dir):
        self.query = query
        self.out_dir = pathlib.Path(out_dir)
        self.timeout = 1
        self.pg_count = 1
        self.down_count = 1
        self.visited = set()
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                                      'Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}

    def get_request_url(self):
        img_type = '+filterui:photo-photo'
        f_query = urllib.parse.quote_plus(self.query)
        return f'https://www.bing.com/images/async?q={f_query}&first={str(self.pg_count)}&qft={img_type}&count=20'

    def get_file_path(self, url):
        path = urllib.parse.urlsplit(url).path
        filename = posixpath.basename(path).split('?')[0]
        file_type = filename.split(".")[-1]
        if file_type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "jpg"]:
            file_type = "jpg"
        return self.out_dir.joinpath("Image_{}.{}".format(str(self.down_count), file_type))

    def download_image(self, url):
        try:
            request = urllib.request.Request(url, None, self.headers)
            image = urllib.request.urlopen(request, timeout=self.timeout).read()
            with open(self.get_file_path(url), 'wb') as f:
                f.write(image)
            self.down_count += 1
        except Exception as e:
            print(f'Error: {e}')

    def download_next_page(self):
        request_url = self.get_request_url()
        request = urllib.request.Request(request_url, None, headers=self.headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf8')
        if html == "":
            print("[%] No more images are available")
        urls = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

        for url in urls:
            if url not in self.visited:
                self.visited.add(url)
                self.download_image(url)

        self.pg_count += 1
