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

from Tools import ImageProvider, ImageUploader, ShareTools
import pyperclip
import os
import re


class ImageMigrator:
    def __init__(self, image_uploader: ImageUploader.ImageUploader):
        self.image_uploader = image_uploader
        self.request_image_provider = None
        self.local_image_provider = None

        # for statistics
        self.total_image_num = None
        self.migrate_succeed_num = None
        self.error_msgs = None

    def init_statistics(self):
        self.total_image_num = 0
        self.migrate_succeed_num = 0
        self.error_msgs = []

    def get_request_image_provider(self) -> ImageProvider.RequestImageProvider:
        if self.request_image_provider is None:
            self.request_image_provider = ImageProvider.RequestImageProvider()
        return self.request_image_provider

    def get_local_image_provider(self) -> ImageProvider.LocalImageProvider:
        if self.local_image_provider is None:
            self.local_image_provider = ImageProvider.LocalImageProvider()
        return self.local_image_provider

    def url_migrate(self, image_url: str) -> str:
        image_object = self.get_request_image_provider().get_image_object(url=image_url)
        image_link = self.image_uploader.core_worker.get_image_link(image_object)
        return image_link

    def path_migrate(self, image_path: str) -> str:
        image_object = self.get_local_image_provider().get_image_object(path=image_path)
        image_link = self.image_uploader.core_worker.get_image_link(image_object)
        return image_link

    def migrate_link(self, link: str) -> str:
        if not link.startswith('http'):
            if os.path.exists(link):
                new_link = self.path_migrate(link)
                return new_link
            else:
                raise Exception('Image with path :\n' + link + '\nDoes not exits, please check it.')
        else:
            new_link = self.url_migrate(link)
            return new_link

    def migrate_line(self, line: str) -> str:
        links = re.findall('\!\[.*\]\((.*)\)', line)
        num = len(links)
        if num == 0:
            return line

        self.total_image_num += num

        for link in links:
            try:
                new_link = self.migrate_link(link)
            except Exception as Ex:
                self.error_msgs.append(Ex.__str__())
                continue
            line = line.replace(link, new_link)
            self.migrate_succeed_num += 1

        return line

    def migrate_from_file(self, original_file_path: str, destination_directory: str) -> str:
        """
        migrates the images in markdown file to another site or some where else in local directory
        :param original_file_path: the path points to the markdown file itself
        :param destination_directory: the directory path to store the result
        :return: the new Markdown file's path
        """
        if not os.path.exists(original_file_path) or not os.path.exists(destination_directory):
            raise Exception('The file to migrate or the path to migrate to does not exits, please check it.')

        self.init_statistics()

        file_name: str = original_file_path[original_file_path.rfind('/') + 1:]

        new_md_file_path = destination_directory + '/' + file_name
        with open(original_file_path, 'r', encoding='utf8') as fin:
            with open(new_md_file_path, 'w', encoding='utf8') as fout:
                for line in fin:
                    new_line = self.migrate_line(line)
                    fout.write(new_line)

        return new_md_file_path

    def migrate_from_clipboard(self):
        """
        migrates the images in markdown strings in clipboard, to another site or local directory (depends on work_mode)
        """
        src = pyperclip.paste()
        if src is None or len(src) == 0:
            raise Exception('No data found in clipboard.')

        src = src.split('\n')
        new_data = []

        for line in src:
            new_line = self.migrate_line(line)
            new_data.append(new_line)

        new_data = '\n'.join(new_data)
        pyperclip.copy(new_data)

    def encountered_any_error(self) -> bool:
        return len(self.error_msgs) > 0

    def failed_every_link_migration(self) -> bool:
        return self.migrate_succeed_num == 0

    def save_errors_to_local_log_file(self) -> str:
        file_path = ShareTools.get_default_path() + os.path.sep + ShareTools.get_timestamp() + '.log'

        try:
            with open(file_path, 'w') as log_file:
                log_file.write("Total images num to migrate :{total_num}, "
                               "migration succeed :{succeed_num}, "
                               "migration failed :{failed_num}\n\n".format(total_num=self.total_image_num,
                                                                           succeed_num=self.migrate_succeed_num,
                                                                           failed_num=len(self.error_msgs))
                               )

                for msg in self.error_msgs:
                    log_file.write(msg + '\n')
        except Exception as ex:
            raise Exception('Failed to generate the log file in path :\n{log_file_path}'.format(log_file_path=file_path))

        return file_path
