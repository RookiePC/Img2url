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
import os
import requests
import datetime
from Tools import ImageProvider, ShareTools
from OptionsData import Options


class ImageUploader:
    def __init__(self):
        self.option_data: Options = Options()
        self.image_provider = ImageProvider.ClipboardImageProvider()
        self.online_mode_worker = UploaderOnlineState(self)
        self.offline_mode_worker = UploaderOfflineState(self)

        # because the img2url always starts on online mode, so there's nothing to worry
        self.core_worker: UploaderBaseState = self.online_mode_worker

    def switch_mode_worker(self):
        """
        switch the work mode when called, simply switch to another one by checking current
        :return: None
        """
        if self.core_worker == self.online_mode_worker:
            self.core_worker = self.offline_mode_worker
        else:
            self.core_worker = self.online_mode_worker

    def get_formatted_link(self):
        """
        universal interface for acquiring the usable link
        """
        image_object = self.core_worker.get_image_object()
        image_link = self.core_worker.get_image_link(image_object)
        return self.core_worker.format_image_link(image_link=image_link)

    def get_upload_link(self) -> (str, str):
        """
        get the upload link to upload file through, raise Exception if anything wrong
        :return: returns the string of upload link
        """
        try:
            resp = requests.get(
                self.option_data.domain + '/api2/repos/' + self.option_data.upload_repo_id + '/upload-link/',
                headers={'Authorization': 'Token {token}'.format(token=self.option_data.auth_token)},
                timeout=self.option_data.timeout
            )
        except requests.exceptions.RequestException as ex:
            raise Exception('Failed during process with exception:' + ex.strerror)

        return datetime.datetime.now(), resp.json()

    @staticmethod
    def ping_test(url, timeout=None) -> bool:
        """
        runs a ping test to the seafile server, could raise a timeout exception if no respond received within the given
        timeout,
        :param url: the server's url
        :param timeout: default to None means no time restriction
        :return: True if get 200 and a "pong" from server
        """
        res = requests.get(url=url + '/api2/ping/', timeout=timeout)

        if res.status_code == 200 and res.text == '"pong"':
            return True

        return False


"""
         the definition of States 
         they are used to describe the different operations of img2url when it's under different states
"""


class UploaderBaseState:
    def __init__(self, img_uploader: ImageUploader):
        self.img_uploader: ImageUploader = img_uploader
        self.option_data = self.img_uploader.option_data
        self.image_provider = self.img_uploader.image_provider
        self.paste_format = self.option_data.paste_format

    def get_image_object(self) -> bytes:
        pass

    def get_image_link(self, img_data: bytes) -> str:
        pass

    def format_image_link(self, image_link) -> str:
        pass


class UploaderOfflineState(UploaderBaseState):
    def __init__(self, img_uploader: ImageUploader):
        super().__init__(img_uploader)

    def get_image_object(self) -> bytes:
        img_object = self.image_provider.get_image_object(img_type=self.option_data.type)
        if img_object is None:
            raise Exception('Failed to get image object from provider, Got a None')
        return img_object

    def get_image_link(self, img_data: bytes) -> str:
        save_dir = self.option_data.image_save_path + os.path.sep + ShareTools.get_date()

        # if the path does not exists then we create one manually
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        try:
            # forms the full save path
            image_path = save_dir + os.path.sep + ShareTools.get_timestamp() + '.' + self.option_data.type

            # save the content to local file
            with open(image_path, 'wb') as image_file:
                image_file.write(img_data)

            return image_path
        except AttributeError as ex:
            raise Exception('Failed while reading data from img with :' + ex.__str__())

    def format_image_link(self, image_link) -> str:
        image_path = image_link.replace('\\', '/')
        return self.paste_format.replace('{url}', image_path)


class UploaderOnlineState(UploaderBaseState):
    def __init__(self, img_uploader: ImageUploader):
        super().__init__(img_uploader)
        self.upload_link = None
        self.upload_link_gen_time = None

    def pre_check(self):
        try:
            if not self.img_uploader.ping_test(self.option_data.domain, self.option_data.timeout):
                raise Exception('Lost connection with the server.')
        except requests.exceptions.RequestException as ex:
            raise Exception('Something went wrong within the process of server connection test with'
                            ' exception :' + ex.__str__())

    def get_image_object(self) -> bytes:
        # get the bytes object from the provider
        img_object = self.image_provider.get_image_object(img_type=self.option_data.type)
        if img_object is None:
            raise Exception("Failed to get image object from provider, Got a None")
        return img_object

    def get_image_link(self, img_data: bytes) -> str:
        # check if the upload link is empty or if the link is out of date
        if self.upload_link is None or (datetime.datetime.now() - self.upload_link_gen_time).seconds > 1800:

            # then we create a new one and refresh the time record
            self.upload_link_gen_time, self.upload_link = self.img_uploader.get_upload_link()

        # runs the pre check,
        # only ping the server to prevent unwanted disconnecting event for now
        self.pre_check()

        # generate a random file name, it's a must-have in the following process
        image_name = ShareTools.get_timestamp() + '.' + self.option_data.type

        # upload with the requests through the seafile web api
        res = requests.post(
            self.upload_link, data={'filename': image_name, 'parent_dir': '/'},
            files={'file': (image_name, img_data)},
            headers={'Authorization': 'Token {token}'.format(token=self.option_data.auth_token)},
            timeout=self.option_data.timeout
        )

        # check the result by status code
        if res.status_code != 200:
            raise Exception('Upload failed with status code :' + str(res.status_code))

        # generates the repo request link
        url = '{domain}/api2/repos/{repo_id}/file/shared-link/'.format(domain=self.option_data.domain,
                                                                       repo_id=self.option_data.upload_repo_id)

        # the file position
        path = '/{file}'.format(file=image_name)

        # the auth token
        token = 'Token {token}'.format(token=self.option_data.auth_token)

        # send the request to obtain the share link through the web api
        res = requests.put(url, data={'p': path}, headers={'Authorization': token}, timeout=self.option_data.timeout)

        # all other status code would be treated as a process failure
        if res.status_code != 201:
            raise Exception('Failed to get image share link with ' + str(res.status_code))

        # the link in 'Location' is exactly what we need,
        # after acquire that, replace the keyword to get the final usable link
        img_url = res.headers['Location'].replace('/f/', '/thumbnail/') + str(self.option_data.size) + '/' + image_name

        return img_url

    def format_image_link(self, image_link) -> str:
        return self.paste_format.replace('{url}', image_link)
