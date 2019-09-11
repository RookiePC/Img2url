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
from OptionWindow import OptionWindow
from Options_data import Options, WorkMode
import requests


class OptionControl:
    def __init__(self, option_ref: Options):
        super().__init__()

        self.option_window = OptionWindow()
        self.option_data = option_ref
        self.option_window.auth_check_button.clicked.connect(self.on_authenticate_check_clicked)
        self.supported_img_format = [
            'PNG',
            'JPG',
            'BMP'
        ]

    def fill_data(self):
        """
        fills line edit in options window with option_data's content
        :return:
        """
        _window = self.option_window
        _data = self.option_data

        _window.status_label.hide()
        _window.library_comboBox.setCurrentText(_data.upload_repo_id)
        _window.domain_edit.setText(_data.domain)

        # if has the auth token, fill it in the edit and change label, disable the pwd edit
        # shows the library label and combo box
        if _data.auth_token != '':
            _window.status_label.setText('Auth Token:' + _data.auth_token)
            _window.status_label.setStyleSheet('QLabel#status_label {color: green}')
            _window.status_label.show()
            self.list_library()
        # else fill the two edit with empty str, and hide the library relevant content
        else:
            _window.usr_edit.setText('')
            _window.pwd_edit.setText('')
            _window.status_label.setStyleSheet('QLabel#status_label {color: black}')
            _window.status_label.hide()
            _window.library_label.hide()
            _window.library_comboBox.hide()

        # adds the supported type to combo box if does not exits any
        if _window.img_type_combobox.count() == 0:
            for img_type in self.supported_img_format:
                _window.img_type_combobox.addItem(img_type)

        _window.img_type_combobox.setCurrentText(_data.type)

        _window.image_size_edit.setText(str(_data.size))

        _window.paste_format_edit.insertPlainText(_data.paste_format)

        _window.quick_pause_edit.setText(_data.quick_pause_hot_key)

        _window.quick_recover_edit.setText(_data.quick_recover_hot_key)

        _window.log_path_edit.setText(_data.log_save_path)

        # sets the radio button's status with the option data
        if _data.work_mode == WorkMode.key_word_replace_mode:
            _window.keyword_replace_mode_radiobutton.setChecked(True)
            _window.hot_key_mode_radiobutton.setChecked(False)
        else:
            _window.hot_key_mode_radiobutton.setChecked(True)
            _window.keyword_replace_mode_radiobutton.setChecked(False)

        _window.substitute_keyword_edit.setText(_data.substitute_keyword)
        _window.trigger_key_edit.setText(_data.trigger_key)
        _window.timeout_edit.setText(str(_data.timeout))
        _window.ignore_prefix_checkbox.setChecked(_data.ignore_prefix)

        _window.hot_key_edit.setText(_data.hot_key)
        # _window.multi_key_mode_checkbox.setEnabled(_data.multi_key_mode)

    def read_settings(self):
        """
        reads all user's input and load them into _option_data, do not check the input
        :return:
        """
        _window = self.option_window
        _data = self.option_data

        _data.domain = _window.domain_edit.text()

        # sets the auth token if already authenticated
        if _window.status_label.text().startswith('Auth Token'):
            _data.auth_token = _window.status_label.text().split(':')[-1]
            _data.upload_repo_id = _window.library_comboBox.currentText().split(' ^-^ ')[-1]
        else:
            _data.auth_token = ''
            _data.upload_repo_id = ''

        _data.type = _window.img_type_combobox.currentText()
        _data.size = int(_window.image_size_edit.text())
        _data.paste_format = _window.paste_format_edit.toPlainText()
        _data.quick_pause_hot_key = _window.quick_pause_edit.text()
        _data.quick_recover_hot_key = _window.quick_recover_edit.text()
        _data.log_save_path = _window.log_path_edit.text()

        _data.original_work_mode = _data.work_mode
        if _window.keyword_replace_mode_radiobutton.isChecked():
            _data.work_mode = WorkMode.key_word_replace_mode
        else:
            _data.work_mode = WorkMode.hot_key_mode

        _data.substitute_keyword = _window.substitute_keyword_edit.text()
        _data.trigger_key = _window.trigger_key_edit.text()
        _data.timeout = int(_window.timeout_edit.text())
        _data.ignore_prefix = _window.ignore_prefix_checkbox.isChecked()

        _data.hot_key = _window.hot_key_edit.text()
        # _data.multi_key_mode = _window.multi_key_mode_checkbox.isChecked()

    def domain_check(self) -> bool:
        """
        try to get the ping message from the web api using requests
        if seafile service available, 200: "pong" will be returned
        else notify the error and quits.
        :return: True if seafile service available, else False
        """
        domain_edit = self.option_window.domain_edit
        if not domain_edit.text().startswith('http://') and not domain_edit.text().startswith('https://'):
            domain_edit.setText('http://' + domain_edit.text())

        try:
            res = requests.get(domain_edit.text() + '/api2/ping/')
        except requests.exceptions.InvalidSchema as ex:
            self.option_window.pop_message_box('Url problems', ex.strerror)
        except requests.exceptions.ConnectionError as ex:
            self.option_window.pop_message_box('Invalid url', ex.strerror)
        except requests.exceptions.RequestException as ex:
            self.option_window.pop_message_box('Unknown error', ex.strerror)
        else:
            # tests the status code and the response text
            if res.status_code == 200 and res.json() == 'pong':
                return True
            else:
                self.option_window.pop_message_box('Web api check failed', 'Failed to connect to web api, check if '
                                                                           'the service available')
        return False

    def authentication_check(self):
        """
        try to get the auth token with given username and password
        :return: Token if retrieved successfully, else None
        """
        label = self.option_window.status_label

        # try to authenticate with given username and password
        try:
            res = requests.post(self.option_window.domain_edit.text() + '/api2/auth-token/',
                                data={
                                    'username': self.option_window.usr_edit.text(),
                                    'password': self.option_window.pwd_edit.text()
                                })

        # catch all exception with request session,
        except requests.exceptions.RequestException:
            label.setText('Failed during authentication procedure.')
            label.setStyleSheet('QLabel#status_label {color: red}')
            return None

        # check the result code of request
        if res.status_code != 200:
            label.setStyleSheet('QLabel#status_label {color: yellow}')
            label.setText('Authentication failed. Username or Password Wrong')
            return None

        return res.json()['token']

    def list_library(self):
        """
        fetch the list of existing library and fill the combobox with auth token in usr_edit(no check)
        :return: None
        """
        # fetch the data of existing libraries
        try:
            res = requests.get(
                url=self.option_window.domain_edit.text() + '/api2/repos/',
                headers={
                    'Authorization': 'Token {token}'.format(token=self.option_window.status_label.text().split(':')[-1])
                }
            )
        except requests.exceptions.RequestException as ex:
            self.option_window.pop_message_box('Failed fetching libraries', ex.strerror)
            return

        if res.status_code != 200:
            self.option_window.pop_message_box('Warning', 'No library get from seafile service')
            return

        repo_id_set = []
        lib_combo_box = self.option_window.library_comboBox
        lib_combo_box.show()
        self.option_window.library_label.show()

        # filter libraries make sure no duplicated library showed in combo box
        for item in res.json():
            repo_id = item['id']
            if repo_id not in repo_id_set:
                lib_combo_box.addItem(item['name'] + ' ^-^ ' + repo_id)
                repo_id_set.append(repo_id)

    def on_selection_changed(self, text: str):
        self.option_data.upload_repo_id = text.split(' ^-^ ')[-1]

    def on_authenticate_check_clicked(self):
        if not self.domain_check():
            return

        token = self.authentication_check()

        if token is None:
            return

        self.option_window.status_label.show()
        self.option_window.status_label.setText('Auth Token:' + token)
        self.option_window.status_label.setStyleSheet('QLabel#status_label {color: green}')

        self.list_library()

    def show_option_window(self):
        self.option_window.show()

    def hide_option_window(self):
        self.option_window.hide()
