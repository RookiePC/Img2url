"""
MIT License

Copyright (c) 2019 RookiePC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import io
import os
import requests
from PIL import Image
from PIL import ImageGrab


class ImageProvider:
    def __init__(self):
        pass

    def get_image_object(self):
        pass


class ClipboardImageProvider(ImageProvider):
    def __init__(self):
        super().__init__()

    def get_image_object(self, img_type='PNG') -> bytes:
        try:
            img = ImageGrab.grabclipboard()

            if img is None:
                raise Exception('No image found in clipboard')

            with io.BytesIO() as OUTPUT:
                img.save(OUTPUT, format=img_type)
                img_data = OUTPUT.getvalue()

            return img_data

        except AttributeError as error:
            raise Exception('Failed while reading data from img with :' + error.__str__())


class RequestImageProvider(ImageProvider):
    def __init__(self):
        super().__init__()

    def get_image_object(self, url=None) -> bytes:
        if url is None:
            raise Exception("Failed to requests the image, No Url is given for requests!")

        response = requests.get(url, stream=True)

        if response.status_code != 200:
            raise Exception("Failed to requests the image, requests returns with " + response.status_code)

        return response.content


class LocalImageProvider(ImageProvider):
    def __init__(self):
        super().__init__()

    def get_image_object(self, path=None) -> bytes:
        if path is None:
            raise Exception("Failed to get local image, No Path is provided!")

        if not os.path.exists(path):
            raise Exception("Failed to get local image, specific path:\n{path}\nDoes not exists.".format(path=path))

        # find out the image tpye by the type extension string in file name
        # definitely will crash if not on windows platform or file name does not contains a type
        try:
            image_format = path[path.rfind('.') + 1:].upper()
        except Exception as ex:
            raise Exception("Failed to get local image, failed to get image type with Exception:\n" + ex.__str__())

        with io.BytesIO() as OUT:
            with Image.open(path, 'r') as image:
                image.save(OUT, format=image_format)
                img_data = OUT.getvalue()

        return img_data
