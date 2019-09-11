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
import keyboard

from first_attempt import DisplayMode
from img2url import Img2url


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
        self.context.main_window.switch_display(DisplayMode.normal_no_hook)
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
        self.context.main_window.switch_display(DisplayMode.normal_hook_installed)
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
                                                       self.context.key_word_replace_callback,
                                                       triggers=self.context.option_data_ref.trigger_key,
                                                       match_suffix=self.context.option_data_ref.ignore_prefix,
                                                       timeout=self.context.option_data_ref.timeout)

        self.context.context_menu_unhook_ref.triggered.disconnect()
        self.context.context_menu_unhook_ref.triggered.connect(self.quit)

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
        self.context.hot_key_callback()
        self.context.main_window.switch_display(DisplayMode.ready_to_paste)
        # only adds the hot key if no previous hot key exists
        if self.paste_handler is None:
            self.paste_handler = keyboard.add_hotkey('ctrl+v', self.paste_callback)

    def paste_callback(self):
        self.context.main_window.switch_display(DisplayMode.normal_hook_installed)
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

