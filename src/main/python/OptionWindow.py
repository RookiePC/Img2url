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

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox


class OptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName('Options')
        self.setFixedSize(450, 300)

        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.central_widget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.central_widget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.authorization_tab = QtWidgets.QWidget()
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.authorization_tab)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.password_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.username_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.domain_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.status_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.library_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.general_tab = QtWidgets.QWidget()
        self.scrollArea = QtWidgets.QScrollArea(self.general_tab)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.log_path_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image_size_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.paste_format_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image_format_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.workmode_tab = QtWidgets.QWidget()
        self.gridLayout_4 = QtWidgets.QGridLayout(self.workmode_tab)
        self.trigger_key_label = QtWidgets.QLabel(self.workmode_tab)
        self.substitute_keyword_label = QtWidgets.QLabel(self.workmode_tab)
        self.timeout_label = QtWidgets.QLabel(self.workmode_tab)
        self.ignore_prefix_label = QtWidgets.QLabel(self.workmode_tab)
        self.line = QtWidgets.QFrame(self.workmode_tab)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.hot_key_label = QtWidgets.QLabel(self.workmode_tab)

        # local mode part
        self.local_mode_tab = QtWidgets.QWidget()
        self.gridLayout_5 = QtWidgets.QGridLayout(self.local_mode_tab)
        self.directory_label = QtWidgets.QLabel(self.local_mode_tab)
        self.save_directory_edit = QtWidgets.QLineEdit(self.local_mode_tab)
        self.browse_button = QtWidgets.QPushButton(self.local_mode_tab)

        # authorization part
        self.usr_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.pwd_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.domain_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.auth_check_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.library_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)

        # general settings part
        self.img_type_combobox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.image_size_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.log_path_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.paste_format_edit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)

        # work mode part
        self.hot_key_edit = QtWidgets.QLineEdit(self.workmode_tab)
        # self.multi_key_mode_checkbox = QtWidgets.QCheckBox(self.workmode_tab)
        self.hot_key_mode_radiobutton = QtWidgets.QRadioButton(self.workmode_tab)
        self.substitute_keyword_edit = QtWidgets.QLineEdit(self.workmode_tab)
        self.trigger_key_edit = QtWidgets.QLineEdit(self.workmode_tab)
        self.keyword_replace_mode_radiobutton = QtWidgets.QRadioButton(self.workmode_tab)
        self.timeout_edit = QtWidgets.QLineEdit(self.workmode_tab)
        self.ignore_prefix_checkbox = QtWidgets.QCheckBox(self.workmode_tab)

        self.reset_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.on_or_offline_switch_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.save_button = QtWidgets.QPushButton(self.verticalLayoutWidget)

        self.set_up_simple_interaction()
        self.setup_ui()
        self.translate_ui()

    def setup_ui(self):
        self.central_widget.setObjectName("central_widget")

        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 0, 400, 301))

        self.verticalLayout.setContentsMargins(10, 5, 10, 8)
        self.verticalLayout.setSpacing(0)

        self.tabWidget.setMinimumSize(QtCore.QSize(380, 250))
        self.tabWidget.setMaximumSize(QtCore.QSize(380, 250))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideRight)

        self.authorization_tab.setObjectName("authorization_tab")

        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 0, 305, 211))

        self.verticalLayout_2.setContentsMargins(10, 5, 5, 10)
        self.verticalLayout_2.setSpacing(10)

        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(-1, -1, 30, -1)
        self.gridLayout.setSpacing(10)

        self.usr_edit.setMinimumSize(QtCore.QSize(186, 21))
        self.usr_edit.setMaximumSize(QtCore.QSize(186, 21))
        self.usr_edit.setObjectName("usr_edit")
        self.gridLayout.addWidget(self.usr_edit, 1, 2, 1, 1)

        self.gridLayout.addWidget(self.password_label, 2, 1, 1, 1)

        self.pwd_edit.setMinimumSize(QtCore.QSize(186, 21))
        self.pwd_edit.setMaximumSize(QtCore.QSize(186, 21))
        self.pwd_edit.setAutoFillBackground(False)
        self.pwd_edit.setInputMethodHints(QtCore.Qt.ImhHiddenText | QtCore.Qt.ImhNoAutoUppercase |
                                          QtCore.Qt.ImhNoPredictiveText | QtCore.Qt.ImhSensitiveData)
        self.pwd_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd_edit.setObjectName("pwd_edit")
        self.gridLayout.addWidget(self.pwd_edit, 2, 2, 1, 1)

        self.username_label.setMinimumSize(QtCore.QSize(62, 21))
        self.username_label.setMaximumSize(QtCore.QSize(62, 21))
        self.gridLayout.addWidget(self.username_label, 1, 1, 1, 1)

        self.domain_label.setMinimumSize(QtCore.QSize(62, 21))
        self.domain_label.setMaximumSize(QtCore.QSize(62, 21))
        self.gridLayout.addWidget(self.domain_label, 0, 1, 1, 1)

        self.domain_edit.setMinimumSize(QtCore.QSize(186, 21))
        self.domain_edit.setMaximumSize(QtCore.QSize(186, 21))
        self.gridLayout.addWidget(self.domain_edit, 0, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)

        self.status_label.setMaximumSize(QtCore.QSize(300, 40))
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName('status_label')
        self.verticalLayout_2.addWidget(self.status_label)

        self.horizontalLayout_4.setSpacing(0)
        spacer_item = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacer_item)

        self.auth_check_button.setMinimumSize(QtCore.QSize(120, 20))
        self.auth_check_button.setMaximumSize(QtCore.QSize(120, 30))
        self.auth_check_button.setAutoDefault(False)
        self.auth_check_button.setDefault(False)
        self.auth_check_button.setFlat(False)
        self.auth_check_button.setObjectName("auth_check_button")
        self.horizontalLayout_4.addWidget(self.auth_check_button)
        spacer_item1 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacer_item1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_3.setSpacing(0)

        self.library_label.setMinimumSize(QtCore.QSize(62, 21))
        self.library_label.setMaximumSize(QtCore.QSize(62, 21))
        self.horizontalLayout_3.addWidget(self.library_label)
        spacer_item2 = QtWidgets.QSpacerItem(12, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacer_item2)

        self.library_comboBox.setMinimumSize(QtCore.QSize(185, 25))
        self.library_comboBox.setMaximumSize(QtCore.QSize(186, 30))
        self.library_comboBox.setObjectName("library_comboBox")
        self.horizontalLayout_3.addWidget(self.library_comboBox)
        spacer_item3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacer_item3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.authorization_tab, "")

        self.general_tab.setObjectName("general_tab")

        self.scrollArea.setGeometry(QtCore.QRect(-4, -2, 391, 231))
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 371, 261))

        self.gridLayout_2.setContentsMargins(5, 0, 15, -1)
        self.gridLayout_2.setHorizontalSpacing(8)
        self.gridLayout_2.setVerticalSpacing(13)

        self.log_path_label.setMinimumSize(QtCore.QSize(85, 20))
        self.log_path_label.setMaximumSize(QtCore.QSize(85, 20))
        self.gridLayout_2.addWidget(self.log_path_label, 6, 0, 1, 1)

        self.image_size_label.setMinimumSize(QtCore.QSize(85, 20))
        self.image_size_label.setMaximumSize(QtCore.QSize(85, 20))
        self.gridLayout_2.addWidget(self.image_size_label, 2, 0, 1, 1, QtCore.Qt.AlignVCenter)

        self.paste_format_label.setMinimumSize(QtCore.QSize(85, 20))
        self.paste_format_label.setMaximumSize(QtCore.QSize(85, 20))
        self.gridLayout_2.addWidget(self.paste_format_label, 3, 0, 1, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.image_format_label.setMinimumSize(QtCore.QSize(85, 20))
        self.image_format_label.setMaximumSize(QtCore.QSize(85, 20))
        self.gridLayout_2.addWidget(self.image_format_label, 1, 0, 1, 1, QtCore.Qt.AlignVCenter)

        self.img_type_combobox.setMinimumSize(QtCore.QSize(240, 25))
        self.img_type_combobox.setMaximumSize(QtCore.QSize(250, 27))
        self.img_type_combobox.setObjectName("img_type_combobox")
        self.gridLayout_2.addWidget(self.img_type_combobox, 1, 1, 1, 1)

        self.image_size_edit.setMinimumSize(QtCore.QSize(240, 20))
        self.image_size_edit.setObjectName("image_size_edit")
        self.image_size_edit.setValidator(QIntValidator())
        self.image_size_edit.setToolTip('Sets the image size, must be integer within 0 and 1024.')
        self.gridLayout_2.addWidget(self.image_size_edit, 2, 1, 1, 1)

        self.log_path_edit.setObjectName("log_path_edit")
        self.log_path_edit.setToolTip('Not supported yet.')
        self.log_path_edit.setEnabled(False)
        self.gridLayout_2.addWidget(self.log_path_edit, 6, 1, 1, 1)

        self.paste_format_edit.setObjectName("paste_format_edit")
        self.gridLayout_2.addWidget(self.paste_format_edit, 3, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.general_tab, "")

        self.workmode_tab.setObjectName("workmode_tab")

        self.gridLayout_4.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout_4.setHorizontalSpacing(0)

        self.hot_key_edit.setObjectName("hot_key_edit")
        self.gridLayout_4.addWidget(self.hot_key_edit, 7, 1, 1, 1)

        self.hot_key_mode_radiobutton.setObjectName("radioButton_2")
        self.gridLayout_4.addWidget(self.hot_key_mode_radiobutton, 6, 0, 1, 1)

        self.substitute_keyword_edit.setObjectName("substitute_keyword_edit")
        self.gridLayout_4.addWidget(self.substitute_keyword_edit, 1, 1, 1, 1)

        self.trigger_key_edit.setObjectName("trigger_key_edit")
        # TODO: Maybe add a few more trigger key
        self.trigger_key_edit.setEnabled(False)
        self.trigger_key_edit.setToolTip('space is the only supported key for now')
        self.gridLayout_4.addWidget(self.trigger_key_edit, 2, 1, 1, 1)

        self.gridLayout_4.addWidget(self.trigger_key_label, 2, 0, 1, 1)

        self.keyword_replace_mode_radiobutton.setObjectName("radioButton")
        self.gridLayout_4.addWidget(self.keyword_replace_mode_radiobutton, 0, 0, 1, 1)

        self.timeout_edit.setObjectName("timeout_edit")
        self.timeout_edit.setValidator(QIntValidator())
        self.gridLayout_4.addWidget(self.timeout_edit, 3, 1, 1, 1)

        self.gridLayout_4.addWidget(self.hot_key_label, 7, 0, 1, 1)

        self.ignore_prefix_checkbox.setObjectName("ignore_prefix_checkbox")
        self.gridLayout_4.addWidget(self.ignore_prefix_checkbox, 4, 1, 1, 1)

        self.gridLayout_4.addWidget(self.substitute_keyword_label, 1, 0, 1, 1)

        self.gridLayout_4.addWidget(self.timeout_label, 3, 0, 1, 1)

        self.gridLayout_4.addWidget(self.ignore_prefix_label, 4, 0, 1, 1)

        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout_4.addWidget(self.line, 5, 0, 1, 2)
        self.tabWidget.addTab(self.workmode_tab, "")
        self.verticalLayout.addWidget(self.tabWidget, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.gridLayout_5.setContentsMargins(10, 15, 5, 15)
        self.gridLayout_5.setHorizontalSpacing(5)
        self.gridLayout_5.setVerticalSpacing(10)

        self.gridLayout_5.addWidget(self.directory_label, 0, 0, 1, 1)
        self.save_directory_edit.setObjectName('save_directory_edit')
        self.gridLayout_5.addWidget(self.save_directory_edit, 0, 1, 1, 1)
        self.browse_button.setObjectName('browse_button')
        self.gridLayout_5.addWidget(self.browse_button, 0, 2, 1, 1)

        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)

        self.reset_button.setMinimumSize(QtCore.QSize(70, 30))
        self.reset_button.setMaximumSize(QtCore.QSize(70, 30))
        self.reset_button.setObjectName("reset_button")
        self.horizontalLayout_2.addWidget(self.reset_button)
        spacer_item4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacer_item4)

        # loacl mode button between the reset and save buttons
        self.on_or_offline_switch_button.setMinimumSize(QtCore.QSize(100, 30))
        self.on_or_offline_switch_button.setMaximumSize(QtCore.QSize(100, 30))
        self.on_or_offline_switch_button.setObjectName("local_mode_button")
        self.on_or_offline_switch_button.setToolTip('Switch to offline mode, stores all image locally.')
        self.horizontalLayout_2.addWidget(self.on_or_offline_switch_button)

        spacer_item5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacer_item5)

        self.save_button.setMinimumSize(QtCore.QSize(70, 30))
        self.save_button.setMaximumSize(QtCore.QSize(70, 30))
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_2.addWidget(self.save_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.setCentralWidget(self.central_widget)

        self.translate_ui()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Options"))
        self.password_label.setText(_translate("MainWindow", "Password"))
        self.username_label.setText(_translate("MainWindow", "Username"))
        self.domain_label.setText(_translate("MainWindow", "Domain"))
        self.status_label.setText(_translate("MainWindow", "TextLabel"))
        self.library_label.setText(_translate("MainWindow", "Library"))
        self.log_path_label.setText(_translate("MainWindow", "Log path"))
        self.image_size_label.setText(_translate("MainWindow", "Image size"))
        self.paste_format_label.setText(_translate("MainWindow", "Paste format"))
        self.image_format_label.setText(_translate("MainWindow", "Image format"))
        self.trigger_key_label.setText(_translate("MainWindow", "Trigger Key"))
        self.hot_key_label.setText(_translate("MainWindow", "Hot Key"))
        self.substitute_keyword_label.setText(_translate("MainWindow", "Substitute Keyword"))
        self.timeout_label.setText(_translate("MainWindow", "Timeout"))
        self.ignore_prefix_label.setText(_translate("MainWindow", "Ignore Prefix"))
        self.directory_label.setText(_translate("MainWindow", "Save Directory"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.authorization_tab), _translate("MainWindow",
                                                                                             "Authorization"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.general_tab), _translate("MainWindow", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.workmode_tab), _translate("MainWindow", "WorkMode"))

        self.hot_key_mode_radiobutton.setText(_translate("MainWindow", "hot key mode"))
        self.keyword_replace_mode_radiobutton.setText(_translate("MainWindow", "Key word replace mode"))

        self.auth_check_button.setText(_translate("MainWindow", "Authenticate"))
        self.browse_button.setText(_translate("MainWindow", "Browse"))
        self.reset_button.setText(_translate("MainWindow", "Reset"))
        self.on_or_offline_switch_button.setText(_translate("MainWindow", "Offline mode"))
        self.save_button.setText(_translate("MainWindow", "Save"))

    def set_up_simple_interaction(self):
        """
        sets simple interaction on ui, no core function related
        :return: None
        """
        self.keyword_replace_mode_radiobutton.toggled.connect(self.on_keyword_radiobutton_toggled)
        self.hot_key_mode_radiobutton.toggled.connect(self.on_hot_key_radiobutton_toggled)

    def on_keyword_radiobutton_toggled(self):
        if self.keyword_replace_mode_radiobutton.isEnabled():
            self.set_hot_key_elements(False)
            self.set_key_word_replace_elements(True)

    def on_hot_key_radiobutton_toggled(self):
        if self.hot_key_mode_radiobutton.isEnabled():
            self.set_hot_key_elements(True)
            self.set_key_word_replace_elements(False)

    def set_key_word_replace_elements(self, enable: bool):
        """
        disables all relevant elements under key word replace mode
        :param enable: status to set
        :return: None
        """
        self.substitute_keyword_edit.setEnabled(enable)
        # self.trigger_key_edit.setEnabled(enable)
        self.timeout_edit.setEnabled(enable)
        self.ignore_prefix_checkbox.setEnabled(enable)

    def set_hot_key_elements(self, enable: bool):
        """
        disables all relevant elements under hot key mode
        :param enable: status to set
        :return: None
        """
        self.hot_key_edit.setEnabled(enable)
        # self.multi_key_mode_checkbox.setEnabled(enable)

    def pop_message_box(self, title: str, message: str):
        """
        pops a message box to notify something
        :param title: message box title to display
        :param message: message text to display inside the box
        :return: None
        """
        QMessageBox.information(self, title, message, buttons=QMessageBox.Ok)

    def confirm_operation(self, title: str, message: str):
        """
        pops message for user to confirm operation
        :param title: message box title to display
        :param message: message text content to display inside the box
        :return: True if confirms to continue
        """
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        return message_box.exec_() == QMessageBox.Yes


if __name__ == '__main__':
    app = QApplication([])
    option_window = OptionWindow()
    option_window.show()
    sys.exit(app.exec_())
