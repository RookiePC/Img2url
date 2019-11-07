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
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from OptionWindow import OptionWindow
from Options_data import Options, WorkMode
import requests


class OptionControl:
    def __init__(self, option_ref: Options):
        super().__init__()
        # stores the lib-name -> lib-token pair
        self.library_dict = {}

        self.option_window = OptionWindow()
        self.option_data = option_ref
        self.option_window.auth_check_button.clicked.connect(self.on_authenticate_check_clicked)
        self.option_window.on_or_offline_switch_button.clicked.connect(self.on_switch_mode_clicked)
        self.option_window.browse_button.clicked.connect(self.on_browse_button_clicked)
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

        # shows the library label and combo box
        if _data.auth_token != '':
            _window.status_label.setText('Login succeed.')
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

        # clears the text edit before insert action to make sure no duplicated text added
        _window.paste_format_edit.clear()
        _window.paste_format_edit.insertPlainText(_data.paste_format)

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

        _window.save_directory_edit.setText(_data.image_save_path)

    def read_settings(self):
        """
        reads all user's input and load them into _option_data, do not check the input
        :return:
        """
        _window = self.option_window
        _data = self.option_data

        _data.domain = _window.domain_edit.text()

        # sets the auth token if already authenticated
        if _window.status_label.text() == 'Login succeed.':
            _data.upload_repo_id = self.library_dict[_window.library_comboBox.currentText()]
        else:
            _data.auth_token = ''
            _data.upload_repo_id = ''

        _data.type = _window.img_type_combobox.currentText()
        _data.size = int(_window.image_size_edit.text())
        _data.paste_format = _window.paste_format_edit.toPlainText()
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

        _data.image_save_path = _window.save_directory_edit.text()

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
            res = requests.get(domain_edit.text() + '/api2/ping/', timeout=self.option_data.timeout)
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
        # try to authenticate with given username and password
        try:
            res = requests.post(self.option_window.domain_edit.text() + '/api2/auth-token/',
                                data={
                                    'username': self.option_window.usr_edit.text(),
                                    'password': self.option_window.pwd_edit.text()
                                },
                                timeout= self.option_data.timeout
                                )

        # catch all exception with request session,
        except requests.exceptions.RequestException:
            self.option_window.pop_message_box('Authenticate Error', 'Failed during authentication procedure with '
                                                                     'exception.')
            return None

        # check the result code of request
        if res.status_code != 200:
            self.option_window.pop_message_box('Authenticate Failed', 'Authentication failed. Username or Password '
                                                                      'Wrong')
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
                    'Authorization': 'Token {token}'.format(token=self.option_data.auth_token)
                },
                timeout=self.option_data.timeout
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

        temp_dict = {}
        lib_combo_box.clear()
        # filter libraries make sure no duplicated library showed in combo box
        for item in res.json():
            repo_id = item['id']
            if repo_id not in repo_id_set:
                combo_box_item = item['name']
                lib_combo_box.addItem(combo_box_item)

                temp_dict[combo_box_item] = repo_id

                repo_id_set.append(repo_id)

        self.library_dict = temp_dict

        for name, repo_id in self.library_dict.items():
            if repo_id == self.option_data.upload_repo_id:
                lib_combo_box.setCurrentText(name)
                return

        self.option_data.upload_repo_id = None
        self.option_window.pop_message_box('Error', 'Library with id {repo_id} is missing.\nPlease re-select the '
                                                    'upload library'.format(repo_id=self.option_data.upload_repo_id))

    def on_authenticate_check_clicked(self):
        """
        Does the authenticate process and shows the hidden elements inside the window, including :
        status label : used to surface auth token.
        library label : to tell what the combo box is next to it
        combobox: list all library in authenticated account.
        :return: None, Exception would be thrown if anything wrong inside any steps.
        """
        if not self.domain_check():
            return

        token = self.authentication_check()

        if token is None:
            return

        self.option_window.status_label.show()
        self.option_window.status_label.setText('Login succeed.')
        self.option_data.auth_token = token
        self.option_window.status_label.setStyleSheet('QLabel#status_label {color: green}')

        self.list_library()

    def show_option_window(self):
        self.fill_data()
        self.option_window.show()

    def paste_format_check(self):
        """
        Checks if the paste format data is legal, the rule for now is that it must contain at least one '{url}'
        for later replacement when triggered.
        :return: None, if anything wrong, Exception would be thrown to surface the issue.
        """
        text = self.option_window.paste_format_edit.toPlainText()
        if '{url}' not in text:
            raise Exception('Paste format should contain at least one keyword "{url}"')

    def substitute_keyword_check(self):
        """
        checks the content in substitute keyword line edit, to ensure the key is supported on relate platform.
        :return: None
        """
        # if on macOS, check if the substitute keyword contains special keys
        keyword_text: str = self.option_window.substitute_keyword_edit.text()
        if len(keyword_text) == 0:
            raise Exception('Substitute keyword cant be empty!')
        if self.option_data.platform == 'darwin':
            if not keyword_text.isalnum():
                raise Exception('Special keys in keyword listening is not supported on MacOS yet.')

    def on_browse_button_clicked(self):
        """
        fills the save directory line edit with directory dialog
        :return: None
        """
        save_path: str = str(QFileDialog.getExistingDirectory(self.option_window, "Select Directory To Store Image"))
        if save_path is not None and len(save_path) != 0:
            self.option_window.save_directory_edit.setText(save_path)
            self.option_data.image_save_path = save_path

    def on_switch_mode_clicked(self):
        """
        switch the online or offline mode
        :return:
        """
        auth_tab: QtWidgets.QWidget = self.option_window.authorization_tab
        local_mode_tab: QtWidgets.QWidget = self.option_window.local_mode_tab
        tab: QtWidgets.QTabWidget = self.option_window.tabWidget
        switch_button: QtWidgets.QPushButton = self.option_window.on_or_offline_switch_button

        # check the status of auth_tab to determine the current mode
        # authorization tab enabled means we are currently on online mode
        if auth_tab.isEnabled():
            # then we switch to offline work mode
            auth_tab.setEnabled(False)

            tab.addTab(local_mode_tab, "Local mode")

            # set the active tab to the newly added one
            tab.setCurrentIndex(tab.indexOf(local_mode_tab))

            # sets the directory path for image storing
            self.option_window.save_directory_edit.setText(self.option_data.image_save_path)

            # change the flag
            self.option_data.work_offline = True
            switch_button.setText('Online mode')

        # else we are currently offline mode
        else:
            # do the online switching work
            # enables the auth tab
            auth_tab.setEnabled(True)

            # set the active tab to the authorization tab
            tab.setCurrentIndex(tab.indexOf(auth_tab))

            # remove the local mode tab
            tab.removeTab(tab.indexOf(local_mode_tab))

            # change the flag
            self.option_data.work_offline = False
            switch_button.setText('Offline mode')
