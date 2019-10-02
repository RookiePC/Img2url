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
import pyperclip
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from Image_uploader import ImageUploader
from floating_view import FloatingWidget, DisplayMode
from Option_control import OptionControl
from Options_data import WorkMode
import keyboard
import floating_view
import pynput


class Img2url(QObject):
    warning_signal = pyqtSignal(str, str)
    error_signal = pyqtSignal(str, str)

    def __init__(self, app_: QtWidgets.QApplication):
        super().__init__()
        self.main_window = FloatingWidget(app_.primaryScreen())
        app_.setQuitOnLastWindowClosed(False)
        self.image_uploader = ImageUploader()
        self.option_data_ref = self.image_uploader.option_data
        self.option_control = OptionControl(self.image_uploader.option_data)
        self.option_control.fill_data()
        self.option_window_ref = self.option_control.option_window

        if self.option_data_ref.platform == 'darwin':
            self.keyboard_controller = pynput.keyboard.Controller()

        self.option_window_ref.save_button.clicked.connect(self.on_save_clicked)
        self.option_window_ref.reset_button.clicked.connect(self.on_reset_clicked)

        self.context_menu_quick_hook_ref = self.main_window.menu_action_quick_hook
        self.context_menu_unhook_ref = self.main_window.menu_action_unhook

        self.main_window.menu_action_options.triggered.connect(self.option_control.show_option_window)

        self.warning_signal.connect(self.main_window.pop_warning)
        self.error_signal.connect(self.main_window.pop_error)

        self.state = None

        self.unhook_keyword_state = UnhookKeywordState(self)
        self.unhook_hotkey_state = UnhookHotKeyState(self)
        self.keyword_hook_state = KeywordHookState(self)
        self.hot_key_state = HotKeyHookState(self)
        self.error_state = ErrorState(self)

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
        image_name = self.image_uploader.upload_image()

        shared_link = self.image_uploader.get_image_share_link(image_name)

        return self.image_uploader.form_image_url(shared_link, image_name)

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
            # run a substitute keyword check
            self.option_control.substitute_keyword_check()

            # check the paste format, make sure there's one '{url}' in it at least.
            self.option_control.paste_format_check()

            # read settings from window
            self.option_control.read_settings()

            # save to config
            self.option_control.option_data.save_config_to_local()

            # refresh the upload link in case of the library selection changed
            self.image_uploader.get_upload_link()

            if self.option_data_ref.original_work_mode != self.option_data_ref.work_mode:
                self.reset_state()
        except Exception as ex:
            # notify user if anything wrong with the process
            self.error_signal.emit('Save Failed', ex.__str__())
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
                self.error_signal.emit('Reset Failed', ex.__str__())


class Img2urlState:
    def enter(self):
        pass

    def quit(self):
        pass

    def reset(self):
        """
        clear current state and jump to opposite state
        triggered if user switched workmode in options
        :return: None
        """
        pass


class UnhookState(Img2urlState):
    def __init__(self, context: Img2url):
        self.context = context

    def enter(self):
        """
        enters unhook state, the appearance and context menu is the only job for now
        :return: None
        """
        self.context.main_window.switch_display(floating_view.DisplayMode.normal_no_hook)
        self.context.context_menu_quick_hook_ref.setEnabled(True)
        self.context.context_menu_unhook_ref.setEnabled(False)


class UnhookKeywordState(UnhookState):
    def __init__(self, context: Img2url):
        super().__init__(context)

    def enter(self):
        # do the display work
        super().enter()
        # clear previous slots
        self.context.context_menu_quick_hook_ref.triggered.disconnect()
        # sets the action of click event of both quick_hook and unhook context menu
        self.context.context_menu_quick_hook_ref.triggered.connect(self.quick_hook_event)

    def quick_hook_event(self):
        """
        call the quit and switch the state to hooked state
        :return:
        """
        self.quit()
        self.context.state = self.context.keyword_hook_state
        self.context.state.enter()


class UnhookHotKeyState(UnhookState):
    def __init__(self, context: Img2url):
        super().__init__(context)

    def enter(self):
        # do the display work
        super().enter()
        # clear previous slots
        self.context.context_menu_quick_hook_ref.triggered.disconnect()
        # sets the action of quick hook clicking
        self.context.context_menu_quick_hook_ref.triggered.connect(self.quick_hook_event)

    def quick_hook_event(self):
        self.quit()
        self.context.state = self.context.hot_key_state
        self.context.state.enter()


class HookState(Img2urlState):
    def __init__(self, context: Img2url):
        self.context = context

    def enter(self):
        self.context.main_window.switch_display(floating_view.DisplayMode.normal_hook_installed)
        self.context.context_menu_quick_hook_ref.setEnabled(False)
        self.context.context_menu_unhook_ref.setEnabled(True)


class KeywordHookState(HookState):
    def __init__(self, context: Img2url):
        super().__init__(context)
        self.hook_handler = None

    def enter(self):
        """
        sets up the key word hook and the unhook state
        :return:
        """
        super().enter()
        self.hook_handler = keyboard.add_word_listener(self.context.option_data_ref.substitute_keyword,
                                                       self.key_word_replace_callback,
                                                       triggers=self.context.option_data_ref.trigger_key,
                                                       match_suffix=self.context.option_data_ref.ignore_prefix,
                                                       timeout=self.context.option_data_ref.timeout)

        self.context.context_menu_unhook_ref.triggered.disconnect()
        self.context.context_menu_unhook_ref.triggered.connect(self.quit)

    def key_word_replace_callback(self):
        """
        for key word substitute mode, clears the substitute key word and write the formatted url
        :return: None
        """
        try:
            formatted_url = self.context.image_to_url_core()
            if self.context.option_data_ref.platform == 'darwin':
                replacement = formatted_url
                # uses pynput to produce backspace because keyboard cant do that for now.
                for i in range(len(self.context.option_data_ref.substitute_keyword) + 1):
                    self.context.keyboard_controller.press(pynput.keyboard.Key.backspace)
            else:
                replacement = '\b' * (len(self.context.option_data_ref.substitute_keyword) + 1) + formatted_url
            keyboard.write(replacement)
        except Exception as ex:
            self.context.error_signal.emit('Key word replace failed', ex.__str__())

    def quit(self):
        # remove existing key word listener
        keyboard.remove_word_listener(self.hook_handler)
        self.context.state = self.context.unhook_keyword_state
        self.context.state.enter()

    def reset(self):
        keyboard.remove_word_listener(self.hook_handler)


class HotKeyHookState(HookState):
    def __init__(self, context: Img2url):
        super().__init__(context)
        self.hook_handler = None
        self.paste_handler = None

    def enter(self):
        super().enter()
        self.hook_handler = keyboard.add_hotkey(self.context.option_data_ref.hot_key, self.hot_key_callback)
        self.context.context_menu_unhook_ref.triggered.disconnect()
        self.context.context_menu_unhook_ref.triggered.connect(self.quit)

    def hot_key_callback(self):
        """
        for hot key mode call back, only does the core job and copy it to clipboard
        :return: None
        """
        try:
            pyperclip.copy(self.context.image_to_url_core())
        except Exception as ex:
            self.context.error_signal.emit('Core Process Failed', ex.__str__())
        else:
            self.context.main_window.switch_display(floating_view.DisplayMode.ready_to_paste)
            # only adds the hot key if no previous hot key exists
            if self.paste_handler is None:
                self.paste_handler = keyboard.add_hotkey('ctrl+v', self.paste_callback)

    def paste_callback(self):
        self.context.main_window.switch_display(floating_view.DisplayMode.normal_hook_installed)
        keyboard.remove_hotkey(self.paste_handler)
        self.paste_handler = None

    def quit(self):
        self.reset()
        self.context.state = self.context.unhook_hotkey_state
        self.context.state.enter()

    def reset(self):
        keyboard.remove_hotkey(self.hook_handler)
        if self.paste_handler is not None:
            keyboard.remove_hotkey(self.paste_handler)
            self.paste_handler = None


class ErrorState(Img2urlState):
    def __init__(self, context: Img2url):
        self.context = context

    def enter(self):
        self.context.main_window.switch_display(DisplayMode.cant_work_normally)
        self.context.main_window.show_tray_icon_message("Fatal error", "Img2url had run into an fatal error, quiting.")
        self.context.main_window.context_menu_quit_clicked()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication([])
    window = Img2url(app)
    window.show()
    sys.exit(app.exec_())