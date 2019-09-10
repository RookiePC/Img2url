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
        self.main_window.menu_action_options.triggered.connect(self.option_control.show_option_window)
        self.main_window.menu_action_quick_hook.triggered.connect(self.quick_hook_context_menu_clicked)
        self.main_window.menu_action_unhook.triggered.connect(self.unhook_context_menu_clicked)
        self.handler_record = None

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
            self.main_window.switch_status(DisplayMode.ready_to_paste)
        except Exception as ex:
            OptionWindow.pop_message_box('Error', ex.__str__())

    def quick_hook_context_menu_clicked(self):
        """
        adds the key listener with data in option, effects the context menu item Quick hoot and Unhook
        :return: None
        """
        try:
            self.setup_listener()
        except Exception as ex:
            OptionWindow.pop_message_box('Set listener error', ex.__str__())
            return

        self.main_window.menu_action_quick_hook.setEnabled(False)
        self.main_window.menu_action_unhook.setEnabled(True)

    def unhook_context_menu_clicked(self):
        """
        remove the existing listener, effects the status of item Quick hook and Unhook in context menu
        :return:
        """
        try:
            self.remove_listener()
        except Exception as ex:
            OptionWindow.pop_message_box('Remove listener error', ex.__str__())
            return

        self.main_window.menu_action_unhook.setEnabled(False)
        self.main_window.menu_action_quick_hook.setEnabled(True)

    def setup_listener(self):
        """
        sets the key listener according to the mode and relevant settings.
        :return:None
        """
        # add new handler according to the settings
        if self.option_data_ref.work_mode == WorkMode.key_word_replace_mode:
            self.handler_record = keyboard.add_word_listener(self.option_data_ref.substitute_keyword,
                                                             self.key_word_replace_callback,
                                                             triggers=self.option_data_ref.trigger_key,
                                                             match_suffix=self.option_data_ref.ignore_prefix,
                                                             timeout=self.option_data_ref.timeout)
        else:
            self.handler_record = keyboard.add_hotkey(self.option_data_ref.hot_key, self.hot_key_callback)

        # change the floating widget status
        self.main_window.switch_status(DisplayMode.normal_hook_installed)

    def remove_listener(self):
        """
        remove existing listener
        :return: None
        """
        # if already registered listener, remove it
        if self.handler_record is not None:
            if self.option_data_ref.work_mode == WorkMode.key_word_replace_mode:
                keyboard.remove_word_listener(self.handler_record)
            else:
                keyboard.remove_hotkey(self.handler_record)
            self.handler_record = None
        self.main_window.switch_status(DisplayMode.normal_no_hook)
        self.main_window.menu_action_unhook.setEnabled(False)
        self.main_window.menu_action_quick_hook.setEnabled(True)

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
            self.remove_listener()

            # read settings from window
            self.option_control.read_settings()

            # save to config
            self.option_control.option_data.save_config_to_local()

            # refresh the upload link in case of the library selection changed
            self.image_uploader.upload_link = self.image_uploader.get_upload_link()
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
                self.remove_listener()
                self.option_control.option_data.reset_all()
                self.option_control.option_data.save_config_to_local()
                self.option_control.fill_data()
            except Exception as ex:
                OptionWindow.pop_message_box('Reset Error', ex.__str__())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Img2url(app)
    window.show()
    sys.exit(app.exec_())
