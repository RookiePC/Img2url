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
import sys

import pyperclip
from PySide2 import QtWidgets
from Image_uploader import ImageUploader
from first_attempt import FloatingWidget, DisplayMode
from Option_control import OptionControl
from OptionWindow import OptionWindow
from Options_data import WorkMode
import keyboard

import img2url_state


class Img2url:
    def __init__(self, app_: QtWidgets.QApplication):
        self.main_window = FloatingWidget(app_.primaryScreen())
        self.image_uploader = ImageUploader()
        self.option_data_ref = self.image_uploader.option_data
        self.option_control = OptionControl(self.image_uploader.option_data)
        self.option_control.fill_data()
        self.option_window_ref = self.option_control.option_window

        self.option_window_ref.save_button.clicked.connect(self.on_save_clicked)
        self.option_window_ref.reset_button.clicked.connect(self.on_reset_clicked)

        self.context_menu_quick_hook_ref = self.main_window.menu_action_quick_hook
        self.context_menu_unhook_ref = self.main_window.menu_action_unhook

        self.main_window.menu_action_options.triggered.connect(self.option_control.show_option_window)

        self.state = None

        self.unhook_keyword_state = img2url_state.UnhookKeywordState(self)
        self.unhook_hotkey_state = img2url_state.UnhookHotKeyState(self)
        self.keyword_hook_state = img2url_state.KeywordHookState(self)
        self.hot_key_state = img2url_state.HotKeyHookState(self)
        self.error_state = img2url_state.ErrorState(self)

        self.reset_state()

    def reset_state(self):
        if self.state is not None:
            self.state.reset()

        if self.option_data_ref.work_mode == WorkMode.key_word_replace_mode:
            self.state = self.unhook_keyword_state
        elif self.option_data_ref.work_mode == WorkMode.hot_key_mode:
            self.state = self.unhook_hotkey_state

        self.state.enter()

    def image_to_url_core(self) -> str:
        """
        perform a series of process to grab image from clipboard, upload, get share link, parse into formatted url
        raises Exception inside core function call
        :return: formatted url of image in clipboard
        """
        if self.image_uploader.upload_link is None:
            self.image_uploader.upload_link = self.image_uploader.get_upload_link()

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
            OptionWindow.pop_message_box('Error', ex.__str__())

    def hot_key_callback(self):
        """
        for hot key mode call back, only does the core job and copy it to clipboard
        :return: None
        """
        try:
            pyperclip.copy(self.image_to_url_core())
        except Exception as ex:
            OptionWindow.pop_message_box('Error', ex.__str__())

    def show(self):
        self.main_window.show()

    def on_save_clicked(self):
        """
        respond the save button click event in option window:
        1. remove exiting keyboard listener to prevent multi-listener on one hot key or keyword
        2. reads settings from the options window
        3. saves them into the local config file
        4. refresh the upload link in case of the selection changed
        pops message box and quits the function if any steps above went wrong
        else hide the window if reaches the end
        :return:None
        """
        try:
            # read settings from window
            self.option_control.read_settings()

            # save to config
            self.option_control.option_data.save_config_to_local()

            # refresh the upload link in case of the library selection changed
            self.image_uploader.upload_link = self.image_uploader.get_upload_link()

            if self.option_data_ref.original_work_mode != self.option_data_ref.work_mode:
                self.reset_state()
        except Exception as ex:
            # notify user if anything wrong with the process
            OptionWindow.pop_message_box('Save Error', ex.__str__())
            return

        # if nothing went wrong then close the option window
        self.option_window_ref.hide()

    def on_reset_clicked(self):
        """
        handles reset button click event, will ask for confirm to continue
        1. remove existing listener to avoid potential conflicts
        2. resets all data in options
        3. save data to local config file
        4. fill those data into option window
        :return: None
        """
        if self.option_control.option_window.confirm_operation('Please Confirm', 'The reset process will clear all '
                                                                                 'settings and restore initial '
                                                                                 'settings, confirm to continue?'):
            try:
                self.option_control.option_data.reset_all()
                self.option_control.option_data.save_config_to_local()
                self.option_control.fill_data()
                self.reset_state()
            except Exception as ex:
                OptionWindow.pop_message_box('Reset Error', ex.__str__())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Img2url(app)
    window.show()
    sys.exit(app.exec_())
