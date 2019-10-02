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
import requests
import io
import datetime
from PIL import ImageGrab
from Options_data import Options


class ImageUploader:
    def __init__(self):
        self.option_data: Options = Options()
        self.upload_link = None
        self.last_get_up_link_time = None

    def get_upload_link(self):
        """
        get the upload link to upload file through, raise Exception if anything wrong
        :return: returns the string of upload link
        """
        try:
            resp = requests.get(
                self.option_data.domain + '/api2/repos/' + self.option_data.upload_repo_id + '/upload-link/',
                headers={'Authorization': 'Token {token}'.format(token=self.option_data.auth_token)}
            )
        except requests.exceptions.RequestException as ex:
            raise Exception('Failed during process with exception:' + ex.strerror)

        # stores the upload link get time for later use
        self.last_get_up_link_time = datetime.datetime.now()

        # fills the upload_link
        self.upload_link = resp.json()

    @staticmethod
    def get_timestamp():
        """
        returns a local timestamp string
        :return: string with format yy-mm-dd-HH-MM-SS
        """
        return datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S')

    def get_clipboard_img(self):
        """
        use pillow module to read image in clipboard, and convert it to binary data, raise Exception if anything wrong
        :return: specified img object with given format
        """
        try:
            img = ImageGrab.grabclipboard()

            if img is None:
                raise Exception('No image found in clipboard')

            with io.BytesIO() as OUTPUT:
                img.save(OUTPUT, format=self.option_data.type)
                img_data = OUTPUT.getvalue()

            return img_data

        except AttributeError as error:
            raise Exception('Failed while reading data from img with :' + error.__str__())

    def upload_image(self):
        """
        upload image object to seafile service.
        :return: image name if succeed else raise Exception
        """
        if self.upload_link is None or (datetime.datetime.now() - self.last_get_up_link_time).seconds > 1800:
            self.get_upload_link()

        image_name = self.get_timestamp() + '.' + self.option_data.type
        image_content = self.get_clipboard_img()

        res = requests.post(
            self.upload_link, data={'filename': image_name, 'parent_dir': '/'},
            files={'file': (image_name, image_content)},
            headers={'Authorization': 'Token {token}'.format(token=self.option_data.auth_token)}
        )
        if res.status_code == 200:
            return image_name
        else:
            raise Exception('Upload failed with status code :' + str(res.status_code))

    def get_image_share_link(self, image_name):
        """
        fetch given image's share link from seafile service, note that the share link cant be used as url directly
        using upload_repo_id and auth_token from option_data
        :param image_name: the image_name of file to fetch
        :return: the share link if succeed else raises the Exception
        """
        url = '{domain}/api2/repos/{repo_id}/file/shared-link/'.format(domain=self.option_data.domain,
                                                                       repo_id=self.option_data.upload_repo_id)
        path = '/{file}'.format(file=image_name)
        token = 'Token {token}'.format(token=self.option_data.auth_token)

        res = requests.put(url, data={'p': path}, headers={'Authorization': token})

        # all other status code would be treated as a process failure
        if res.status_code == 201:
            return res.headers['Location']
        else:
            raise Exception('Failed to get image share link with ' + str(res.status_code))

    def form_image_url(self, share_link: str, image_name: str) -> str:
        """
        foms a image url from given share link, note that this is only capable with seafile's share link
        :param share_link:
        :param image_name:
        :return: the image url contained in given format in option_data
        """
        img_url = share_link.replace('/f/', '/thumbnail/') + str(self.option_data.size) + '/' + image_name
        return self.option_data.paste_format.replace('{url}', img_url)
