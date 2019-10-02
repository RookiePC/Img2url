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
import sys
import enum
import configparser


class WorkMode(enum.Enum):
    key_word_replace_mode = 1
    hot_key_mode = 2


class Options:
    def __init__(self):
        super().__init__()
        self.platform: str = sys.platform
        # config object initialization
        self.config_parser: configparser.ConfigParser = configparser.ConfigParser()

        # authorization and requests relevant
        self.domain: str = ''
        self.auth_token: str = ''
        self.upload_repo_id: str = ''

        # working mode
        self.work_mode: WorkMode = WorkMode.key_word_replace_mode
        self.original_work_mode: WorkMode = self.work_mode

        # image settings
        self.type: str = ''
        self.size: str = ''

        # paste format settings
        self.paste_format: str = ''

        # replace keyword mode
        self.substitute_keyword: str = ''
        self.ignore_prefix: bool = False
        self.timeout: int = 0
        self.trigger_key: str = ''

        # hot-key mode
        self.hot_key: str = ''

        # file save
        self.log_save_path: str = ''

        # directory to save image, CAUTION: wont be saved in the config file
        self.image_save_path: str = ''

        # consts that wouldn't change
        self.config_file_name: str = 'img2url.ini'

        self.section_names = [
            'authorization',
            'work mode',
            'general'
        ]
        # inits the config object first
        self.config_init()

        # after all member variable declared, inits them with reset method(this would inits the config object not the
        # file) do this before read from local to avoid unexpected error shuts down the application
        self.reset_all()

        # if read from local failed which means the config does not exists or not complete, then we save one manually
        if not self.read_local_config_file():
            self.save_config_to_local()

    def config_init(self):
        """
        inits the config object by adding given sections
        :return:None
        """
        # add sections for each part of setting
        for name in self.section_names:
            self.config_parser.add_section(name)

    def reset_all(self):
        """
        reset all variable to default value using all other reset method and updates the config file
        does not trigger a config saving action after all the reset process
        :return:None
        """
        self.reset_authorization_settings()
        self.save_authorization_settings()

        self.reset_general_settings()
        self.save_general_settings()

        self.reset_work_mode_settings()
        self.save_work_mode_settings()

        # resets the image save path here since we don't actually stores it in config file
        # and it does not belong to any section we have
        self.image_save_path = self.get_default_path()

    def reset_authorization_settings(self):
        """
        resets the web-api related part, set domain, auth_token, upload_repo_id to None.
        does not trigger a config saving action
        :return: None
        """
        self.domain = ''
        self.auth_token = ''
        self.upload_repo_id = ''

    def save_authorization_settings(self):
        """
        updates(or sets if not exists) authorization settings in config objec
        does not trigger save to local action
        :return: None
        """
        self.config_parser['authorization'] = {
            'auth_token': self.auth_token,
            'domain': self.domain,
            'upload_repo_id': self.upload_repo_id
        }

    def reset_general_settings(self):
        """
        resets settings included in general settings,
        type : PNG
        size : 1024
        paste_format : ![]({url})
        quick_pause_hot_key : ctrl+alt+p
        quick_recover_hot_key : ctrl+alt+r
        log_save_path : %USER%/img2url
        :return:
        """
        self.type: str = 'PNG'
        self.size: int = 1024
        self.paste_format: str = r'![]({url})'
        self.log_save_path = self.get_default_path()

    def save_general_settings(self):
        """
        updates(or sets) general settings in config object
        does not trigger a write to local action
        :return: None
        """
        self.config_parser['general'] = {
            'type': self.type,
            'size': self.size,
            'paste_format': self.paste_format.replace('\n', '<&br />'),
            'log_path': self.log_save_path
        }

    def reset_work_mode_settings(self):
        """
        resets settings in work mode settings, does not change current workmode, but reset relevant settings
        substitute_keyword: @@
        trigger_key : space
        ignore_prefix: True
        timeout: 200
        hot_key: f1
        :return:
        """
        # self.work_mode = WorkMode.key_word_replace_mode
        self.substitute_keyword = '@@'
        self.ignore_prefix = True
        self.trigger_key = 'space'
        self.timeout = 200
        self.hot_key = 'f1'
        # self.multi_key_mode = False

    def save_work_mode_settings(self):
        """
        updates(or sets) work mode settings in config object
        does not trigger a write to local action
        :return: None
        """
        self.config_parser['work mode'] = {
            'work_mode': self.work_mode.__str__(),
            'substitute_keyword': self.substitute_keyword,
            'ignore_prefix': self.ignore_prefix,
            'timeout': self.timeout,
            'trigger_key': self.trigger_key,
            'hot_key': self.hot_key
            # 'multi_key_mode': self.multi_key_mode
        }

    def save_config_to_local(self):
        """
        writes config object to local directly
        does not check content
        :return: None
        """
        self.save_authorization_settings()
        self.save_general_settings()
        self.save_work_mode_settings()
        with open(self.get_default_path() + os.sep + self.config_file_name, 'w') as config_file:
            self.config_parser.write(config_file)

    def read_local_config_file(self) -> bool:
        """
        reads all local settings, returns the operation result
        :return: True if successfully loaded data, else False
        """
        local_config_file = self.get_default_path() + os.sep + self.config_file_name

        # path check
        if not os.path.exists(local_config_file):
            return False

        try:
            # read into memory
            self.config_parser.read(local_config_file)

            # all section check
            for name in self.section_names:
                if name not in self.config_parser:
                    return False

            # read in settings
            self.read_authorization_settings(self.config_parser['authorization'])
            self.read_general_settings(self.config_parser['general'])
            self.read_work_mode_settings(self.config_parser['work mode'])
        except configparser.Error:
            # returns false if anything wrong within the process
            return False

        return True

    def read_authorization_settings(self, authorization_section: configparser.SectionProxy):
        """
        read settings from given sections, if no value found, no value would change
        :param authorization_section: the authorization in config
        :return: None
        """
        self.domain = authorization_section.get('domain', self.domain)
        self.auth_token = authorization_section.get('auth_token', self.auth_token)
        self.upload_repo_id = authorization_section.get('upload_repo_id', self.upload_repo_id)

    def read_general_settings(self, general_section: configparser.SectionProxy):
        """
        read settings from given sections, if no value found, no value would change
        better be called after the reset so the variables won't be None
        :param general_section: the general section in config
        :return: None
        """
        self.type = general_section.get('type', self.type)
        self.size = general_section.getint('size', self.size)
        self.paste_format = general_section.get('paste_format', self.paste_format).replace('<&br />', '\n')
        self.log_save_path = general_section.get('log_path', self.log_save_path)

    def read_work_mode_settings(self, work_mode_section: configparser.SectionProxy):
        """
        read settings from given sections, if no value found, no value would change
        better be called after the reset so the variables won't be None
        :return: None
        """
        # check str to determine the value of enum for the configparser does not support enum type yet
        self.work_mode = work_mode_section.get('work_mode', self.work_mode)

        if WorkMode.hot_key_mode.__str__() == work_mode_section.get('work_mode'):
            self.work_mode = WorkMode.hot_key_mode
        else:
            self.work_mode = WorkMode.key_word_replace_mode

        self.substitute_keyword = work_mode_section.get('substitute_keyword', self.substitute_keyword)
        self.ignore_prefix = work_mode_section.getboolean('ignore_prefix', self.ignore_prefix)
        self.timeout = work_mode_section.getint('timeout', self.timeout)
        self.trigger_key = work_mode_section.get('trigger_key', self.trigger_key)
        self.hot_key = work_mode_section.get('hot_key', self.hot_key)

    @staticmethod
    def get_default_path() -> str:
        """
        returns the default path for config files to store
        checks the path on each call, will create one if doesn't exists one
        :return: the default path (existence checked)
        """
        default_path = os.path.expanduser('~') + os.path.sep + 'img2url'
        if not os.path.exists(default_path):
            # TODO: Handle the mkdir() failure
            os.mkdir(default_path)
        return default_path


if __name__ == '__main__':
    testOption = Options()
