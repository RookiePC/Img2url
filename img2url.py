from PySide2 import QtWidgets
from Image_uploader import ImageUploader
from first_attempt import FloatingWidget
from Option_control import OptionControl
from Options_data import WorkMode
import keyboard


class Img2url:
    def __init__(self):
        self.app = QtWidgets.QApplication([])

        self.main_window = FloatingWidget(self.app.primaryScreen())
        self.image_uploader = ImageUploader()
        self.option_data_ref = self.image_uploader.option_data
        self.option_control = OptionControl(self.image_uploader.option_data)
        self.option_window_ref = self.option_control.option_window
        self.handler_record = None

    def image_to_url_core(self)-> str:
        """
        perform a series of process to grab image from clipboard, upload, get share link, parse into formatted url
        raises Exception inside core function call
        :return: formatted url of image in clipboard
        """
        image_name = self.image_uploader.upload_image()

        shared_link = self.image_uploader.get_image_share_link(image_name)

        return self.image_uploader.form_image_url(shared_link, image_name)

    def key_word_replace_callback(self):
        """
        for key word substitute mode, clears the substitute key word and write the formatted url
        :return: None
        """
        try:
            formatted_url = self.image_to_url_core()
            replacement = '\b' * (len(self.option_data_ref.substitute_keyword) + 1) + formatted_url
            keyboard.write(replacement)
        except Exception as ex:
            self.option_window_ref.pop_message_box('Error', ex.__str__())

    def on_save_clicked(self):
        try:
            # if already registered listener, remove it
            if self.handler_record is not None:
                if self.option_data_ref.work_mode == WorkMode.key_word_replace_mode:
                    keyboard.remove_word_listener(self.handler_record)
                else:
                    keyboard.remove_hotkey(self.handler_record)
                self.handler_record = None

            # read settings from window
            self.option_control.read_settings()

            # save to config
            self.option_control.option_data.save_config_to_local()

            # refresh the upload link in case of the library selection changed
            self.image_uploader.upload_link = self.image_uploader.get_upload_link()

            # if handler exists, remove it
            if self.option_data_ref.work_mode == WorkMode.key_word_replace_mode:
                keyboard.add_word_listener(self.option_data_ref.substitute_keyword,
                                           self.key_word_replace_callback,
                                           triggers=self.option_data_ref.trigger_key,
                                           match_suffix=self.option_data_ref.ignore_prefix,
                                           timeout=self.option_data_ref.timeout)
        except Exception as ex:
            # notify user if anything wrong with the process
            self.option_window_ref.pop_message_box('Error', ex.__str__())


    def on_reset_clicked(self):
        if self.option_control.option_window.confirm_operation('Please Confirm', 'The reset process will clear all '
                                                                                 'settings and restore initial '
                                                                                 'settings, confirm to continue?'):
            self.option_control.option_data.reset_all()
            self.option_control.option_data.save_config_to_local()
            self.option_control.fill_data()
