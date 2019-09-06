import os
import enum

class WorkMode(enum.Enum):
    key_word_replace_mode = 1
    hot_key_mode = 2
    # TODO: local mode


class Options:
    def __init__(self):
        super().__init__()
        # authorization and requests relevant
        self.domain = None
        self.auth_token = None
        self.upload_repo_id = None

        # working mode
        self.work_mode = None

        # image settings
        self.type = None
        self.size = None

        # paste format settings
        self.paste_format = None

        # replace keyword mode
        self.substitute_keyword = None
        self.ignore_prefix = None
        self.timeout = None
        self.trigger_key = None

        # hot-key mode
        self.hot_key = None
        self.multi_key_mode = None

        # quick_pause
        self.quick_pause_hot_key = None
        self.quick_recover_hot_key = None

        # file save
        self.config_save_path = None
        self.log_save_path = None

        # consts that wouldn't change
        self.config_file_name = 'img2url.ini'

    def reset_all(self):
        """
        reset all variable to default value using all other reset method
        trigger a config saving action after all the reset process
        :return:None
        """
        self.reset_authorization_part()
        self.reset_image_settings()
        self.reset_work_mode()
        self.reset_keyword_replace_mode()
        self.reset_quick_hot_key_mode()
        self.reset_file_path()

    def reset_authorization_part(self):
        """
        resets the web-api related part, set domain, auth_token, upload_repo_id to None.
        does not trigger a config saving action
        :return: None
        """
        self.domain = None
        self.auth_token = None
        self.upload_repo_id = None

    def reset_image_settings(self):
        """
        resets image relevant settings, only type and size for now
        type('PNG'), size(1024)
        does not trigger a config saving action
        :return:None
        """
        self.type = "PNG"
        self.size = 1024

    def reset_paste_format(self):
        """
        resets the paste_format('![]({url})') for now, maybe there would be more work to do?
        does not trigger a config saving action
        :return:None
        """
        self.paste_format = r"![]({url))"

    def reset_work_mode(self):
        """
        resets the work_mode(key_word_replace_mode)
        does not trigger a config saving action
        :return:None
        """
        self.work_mode = WorkMode.key_word_replace_mode

    def reset_keyword_replace_mode(self):
        """
        resets substitute_keyword('@@'), ignore_prefix(True), timeout(200), trigger_key('space')
        does not trigger a config saving action
        :return:None
        """
        self.substitute_keyword = "@@"
        self.ignore_prefix = True
        self.timeout = 200
        self.trigger_key = 'space'

    def reset_quick_hot_key_mode(self):
        """
        resets quick_pause_hot_key('ctrl+alt+p'), quick_recover_hot_key('ctrl+alt+r')
        does not trigger a config saving action
        :return:None
        """
        self.quick_pause_hot_key = 'ctrl+alt+p'
        self.quick_recover_hot_key = 'ctrl+alt+r'

    def reset_file_path(self):
        """
        generates a default path under user's directory and make one if it doesn't exists
        reset config_save_path, log_save_path
        :return:None
        """
        default_path = os.path.expanduser('~') + os.path.sep + 'img2url'

        if not os.path.exists(default_path):
            # TODO: Handle the mkdir() failure
            os.mkdir(default_path)

        self.config_save_path = default_path
        self.log_save_path = default_path

