from OptionWindow import OptionWindow
from Options_data import Options, WorkMode


class OptionControl:
    def __init__(self):
        super().__init__()

        self.option_window = OptionWindow()
        self.option_data = Options()

        self.supported_img_format = [
            'PNG',
            'JPG',
            'BMP'
        ]

    def fill_data(self):
        _window = self.option_window
        _data = self.option_data

        _window.status_label.hide()
        _window.library_comboBox.setCurrentText(_data.upload_repo_id)
        _window.domain_edit.setText(_data.domain)

        # if has the auth token, fill it in the edit and change label, disable the pwd edit
        # shows the library label and combo box
        if _data.auth_token != '':
            _window.usr_edit.setText(_data.auth_token)
            _window.username_label.setText('Auth Token')
            _window.pwd_edit.setEnabled(False)
            _window.library_label.show()
            _window.library_comboBox.show()
        # else fill the two edit with empty str, and hide the library relevant content
        else:
            _window.usr_edit = ''
            _window.pwd_edit = ''
            _window.library_label.hide()
            _window.library_comboBox.hide()

        # adds the supported type to combo box if does not exits any
        if _window.img_type_combobox.count() == 0:
            for img_type in self.supported_img_format:
                _window.img_type_combobox.addItem(img_type)

        _window.img_type_combobox.setCurrentText(_data.type)

        _window.image_size_edit.setText(_data.size)

        _window.paste_format_edit.setText(_data.paste_format)

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
        _window.timeout_edit.setText(_data.timeout)
        _window.ignore_prefix_checkbox.setChecked(_data.ignore_prefix)

        _window.hot_key_edit.setText(_data.hot_key)
        _window.multi_key_mode_checkbox.setText(_data.multi_key_mode)

    def read_settings(self):
        _window = self.option_window
        _data = self.option_data

