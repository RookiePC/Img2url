import requests
import io
import time
import pyperclip
from PIL import ImageGrab
from Options_data import Options


class ImageUploader:
    def __init__(self):
        self.option_data: Options = Options()
        self.upload_link = None

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
        return resp.json()

    @staticmethod
    def get_timestamp():
        """
            returns a local timestamp string
            :return: string with format yy-mm-dd-HH-MM-SS
            """
        return time.strftime('%y-%m-%d-%H-%M-%S', time.localtime())

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
        url = '{domain}/api2/repos/{repo_id}/file/shared-link/'.format(domain=self.option_data.domain,
                                                                       repo_id=self.option_data.upload_repo_id)
        path = '/{file}'.format(file=image_name)
        token = 'Token {token}'.format(token=self.option_data.auth_token)

        res = requests.put(url, data={'p': path}, headers={'Authorization': 'Token ' + token})

        if res.status_code == 201:
            return res.headers['Location']
        else:
            raise Exception('Failed to get image share link with ' + str(res.status_code))

    def form_image_url(self, share_link: str, image_name: str) -> str:
        img_url = share_link.replace('/f/', '/thumbnail/') + '/' + str(self.option_data.size) + '/' + image_name
        return self.option_data.paste_format.replace('{url}', img_url)
