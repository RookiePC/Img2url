# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Option_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import sys

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QApplication


class OptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName('Options')
        self.setFixedSize(450, 300)

        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint)

        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.authorization_tab = QtWidgets.QWidget()
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.authorization_tab)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.usr_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.password_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.pwd_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.username_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.domain_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.domain_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.status_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.check_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.library_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.general_tab = QtWidgets.QWidget()
        self.scrollArea = QtWidgets.QScrollArea(self.general_tab)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.quick_pause_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.log_path_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image_size_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.quick_recover_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.paste_format_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image_format_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.img_type_combobox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.image_size_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.quick_pause_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.quick_recover_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.log_path_edit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.paste_format_edit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.workmode_tab = QtWidgets.QWidget()
        self.gridLayout_4 = QtWidgets.QGridLayout(self.workmode_tab)
        self.hot_key_edit = QtWidgets.QLineEdit(self.workmode_tab)
        self.multi_key_mode_checkbox = QtWidgets.QCheckBox(self.workmode_tab)
        self.hot_key_mode_radiobutton = QtWidgets.QRadioButton(self.workmode_tab)
        self.substitute_keyword_edit = QtWidgets.QLineEdit(self.workmode_tab)
        self.trigger_key_edit = QtWidgets.QLineEdit(self.workmode_tab)
        self.label_2 = QtWidgets.QLabel(self.workmode_tab)
        self.keyword_replace_mode_radiobutton = QtWidgets.QRadioButton(self.workmode_tab)
        self.timeout_edit = QtWidgets.QLineEdit(self.workmode_tab)
        self.label_5 = QtWidgets.QLabel(self.workmode_tab)
        self.ignore_prefix_checkbox = QtWidgets.QCheckBox(self.workmode_tab)
        self.label_6 = QtWidgets.QLabel(self.workmode_tab)
        self.label = QtWidgets.QLabel(self.workmode_tab)
        self.label_4 = QtWidgets.QLabel(self.workmode_tab)
        self.label_3 = QtWidgets.QLabel(self.workmode_tab)
        self.line = QtWidgets.QFrame(self.workmode_tab)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.reset_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.save_button = QtWidgets.QPushButton(self.verticalLayoutWidget)

        self.setup_ui()
        self.translate_ui()

    def setup_ui(self):
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 0, 400, 301))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout.setContentsMargins(10, 5, 10, 8)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.tabWidget.setMinimumSize(QtCore.QSize(380, 250))
        self.tabWidget.setMaximumSize(QtCore.QSize(380, 250))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideRight)
        self.tabWidget.setObjectName("tabWidget")

        self.authorization_tab.setObjectName("authorization_tab")

        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 0, 305, 211))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        self.verticalLayout_2.setContentsMargins(10, 0, 5, 10)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(-1, -1, 30, -1)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")

        self.usr_edit.setMinimumSize(QtCore.QSize(186, 21))
        self.usr_edit.setMaximumSize(QtCore.QSize(186, 21))
        self.usr_edit.setObjectName("usr_edit")
        self.gridLayout.addWidget(self.usr_edit, 1, 2, 1, 1)

        self.password_label.setObjectName("password")
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
        self.username_label.setObjectName("username")
        self.gridLayout.addWidget(self.username_label, 1, 1, 1, 1)

        self.domain_label.setMinimumSize(QtCore.QSize(62, 21))
        self.domain_label.setMaximumSize(QtCore.QSize(62, 21))
        self.domain_label.setObjectName("domain")
        self.gridLayout.addWidget(self.domain_label, 0, 1, 1, 1)

        self.domain_edit.setMinimumSize(QtCore.QSize(186, 21))
        self.domain_edit.setMaximumSize(QtCore.QSize(186, 21))
        self.domain_edit.setObjectName("domain_edit")
        self.gridLayout.addWidget(self.domain_edit, 0, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)

        self.status_label.setMaximumSize(QtCore.QSize(300, 40))
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.verticalLayout_2.addWidget(self.status_label)

        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacer_item = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacer_item)

        self.check_button.setMinimumSize(QtCore.QSize(120, 20))
        self.check_button.setMaximumSize(QtCore.QSize(120, 30))
        self.check_button.setAutoDefault(False)
        self.check_button.setDefault(False)
        self.check_button.setFlat(False)
        self.check_button.setObjectName("check_button")
        self.horizontalLayout_4.addWidget(self.check_button)
        spacer_item1 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacer_item1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.library_label.setMinimumSize(QtCore.QSize(62, 21))
        self.library_label.setMaximumSize(QtCore.QSize(62, 21))
        self.library_label.setObjectName("library_label")
        self.horizontalLayout_3.addWidget(self.library_label)
        spacer_item2 = QtWidgets.QSpacerItem(12, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacer_item2)

        self.comboBox.setMinimumSize(QtCore.QSize(185, 25))
        self.comboBox.setMaximumSize(QtCore.QSize(186, 30))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_3.addWidget(self.comboBox)
        spacer_item3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacer_item3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.authorization_tab, "")

        self.general_tab.setObjectName("general_tab")

        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 381, 221))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 371, 261))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayout_3.setObjectName("gridLayout_3")

        self.gridLayout_2.setContentsMargins(5, 0, 15, -1)
        self.gridLayout_2.setHorizontalSpacing(8)
        self.gridLayout_2.setVerticalSpacing(13)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.quick_pause_label.setMinimumSize(QtCore.QSize(85, 20))
        self.quick_pause_label.setMaximumSize(QtCore.QSize(85, 20))
        self.quick_pause_label.setObjectName("quick_pause_label")
        self.gridLayout_2.addWidget(self.quick_pause_label, 4, 0, 1, 1, QtCore.Qt.AlignVCenter)

        self.log_path_label.setMinimumSize(QtCore.QSize(85, 20))
        self.log_path_label.setMaximumSize(QtCore.QSize(85, 20))
        self.log_path_label.setObjectName("log_path_label")
        self.gridLayout_2.addWidget(self.log_path_label, 6, 0, 1, 1)

        self.image_size_label.setMinimumSize(QtCore.QSize(85, 20))
        self.image_size_label.setMaximumSize(QtCore.QSize(85, 20))
        self.image_size_label.setObjectName("image_size_label")
        self.gridLayout_2.addWidget(self.image_size_label, 2, 0, 1, 1, QtCore.Qt.AlignVCenter)

        self.quick_recover_label.setMinimumSize(QtCore.QSize(85, 20))
        self.quick_recover_label.setMaximumSize(QtCore.QSize(85, 20))
        self.quick_recover_label.setObjectName("quick_recover_label")
        self.gridLayout_2.addWidget(self.quick_recover_label, 5, 0, 1, 1)

        self.paste_format_label.setMinimumSize(QtCore.QSize(85, 20))
        self.paste_format_label.setMaximumSize(QtCore.QSize(85, 20))
        self.paste_format_label.setObjectName("paste_format_label")
        self.gridLayout_2.addWidget(self.paste_format_label, 3, 0, 1, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.image_format_label.setMinimumSize(QtCore.QSize(85, 20))
        self.image_format_label.setMaximumSize(QtCore.QSize(85, 20))
        self.image_format_label.setObjectName("image_format_label")
        self.gridLayout_2.addWidget(self.image_format_label, 1, 0, 1, 1, QtCore.Qt.AlignVCenter)

        self.img_type_combobox.setMinimumSize(QtCore.QSize(240, 25))
        self.img_type_combobox.setMaximumSize(QtCore.QSize(250, 27))
        self.img_type_combobox.setObjectName("img_type_combobox")
        self.gridLayout_2.addWidget(self.img_type_combobox, 1, 1, 1, 1)

        self.image_size_edit.setMinimumSize(QtCore.QSize(240, 20))
        self.image_size_edit.setObjectName("image_size_edit")
        self.gridLayout_2.addWidget(self.image_size_edit, 2, 1, 1, 1)

        self.quick_pause_edit.setObjectName("quick_pause_edit")
        self.gridLayout_2.addWidget(self.quick_pause_edit, 4, 1, 1, 1)

        self.quick_recover_edit.setObjectName("quick_recover_edit")
        self.gridLayout_2.addWidget(self.quick_recover_edit, 5, 1, 1, 1)

        self.log_path_edit.setObjectName("log_path_edit")
        self.gridLayout_2.addWidget(self.log_path_edit, 6, 1, 1, 1)

        self.paste_format_edit.setObjectName("paste_format_edit")
        self.gridLayout_2.addWidget(self.paste_format_edit, 3, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.general_tab, "")

        self.workmode_tab.setObjectName("workmode_tab")

        self.gridLayout_4.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout_4.setHorizontalSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.hot_key_edit.setObjectName("hot_key_edit")
        self.gridLayout_4.addWidget(self.hot_key_edit, 7, 1, 1, 1)

        self.multi_key_mode_checkbox.setText("")
        self.multi_key_mode_checkbox.setObjectName("multi_key_mode_checkbox")
        self.gridLayout_4.addWidget(self.multi_key_mode_checkbox, 8, 1, 1, 1)

        self.hot_key_mode_radiobutton.setObjectName("radioButton_2")
        self.gridLayout_4.addWidget(self.hot_key_mode_radiobutton, 6, 0, 1, 1)

        self.substitute_keyword_edit.setObjectName("substitute_keyword_edit")
        self.gridLayout_4.addWidget(self.substitute_keyword_edit, 1, 1, 1, 1)

        self.trigger_key_edit.setObjectName("trigger_key_edit")
        self.gridLayout_4.addWidget(self.trigger_key_edit, 2, 1, 1, 1)

        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 1)

        self.keyword_replace_mode_radiobutton.setObjectName("radioButton")
        self.gridLayout_4.addWidget(self.keyword_replace_mode_radiobutton, 0, 0, 1, 1)

        self.timeout_edit.setObjectName("timeout_edit")
        self.gridLayout_4.addWidget(self.timeout_edit, 3, 1, 1, 1)

        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 7, 0, 1, 1)

        self.ignore_prefix_checkbox.setText("")
        self.ignore_prefix_checkbox.setObjectName("ignore_prefix_checkbox")
        self.gridLayout_4.addWidget(self.ignore_prefix_checkbox, 4, 1, 1, 1)

        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 8, 0, 1, 1)

        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 1, 0, 1, 1)

        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 4, 0, 1, 1)

        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 5, 0, 1, 2)
        self.tabWidget.addTab(self.workmode_tab, "")
        self.verticalLayout.addWidget(self.tabWidget, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.reset_button.setMinimumSize(QtCore.QSize(70, 30))
        self.reset_button.setMaximumSize(QtCore.QSize(70, 30))
        self.reset_button.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.reset_button)
        spacer_item4 = QtWidgets.QSpacerItem(400, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacer_item4)

        self.save_button.setMinimumSize(QtCore.QSize(70, 30))
        self.save_button.setMaximumSize(QtCore.QSize(70, 30))
        self.save_button.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.save_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.setCentralWidget(self.centralwidget)

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
        self.quick_pause_label.setText(_translate("MainWindow", "Quick pause"))
        self.log_path_label.setText(_translate("MainWindow", "Log path"))
        self.image_size_label.setText(_translate("MainWindow", "Image size"))
        self.quick_recover_label.setText(_translate("MainWindow", "Quick recover"))
        self.paste_format_label.setText(_translate("MainWindow", "Paste format"))
        self.image_format_label.setText(_translate("MainWindow", "Image format"))
        self.label_2.setText(_translate("MainWindow", "Trigger Key"))
        self.label_5.setText(_translate("MainWindow", "Hot Key"))
        self.label_6.setText(_translate("MainWindow", "Multi-key Mode"))
        self.label.setText(_translate("MainWindow", "Substitute Keyword"))
        self.label_4.setText(_translate("MainWindow", "Timeout"))
        self.label_3.setText(_translate("MainWindow", "Ignore Prefix"))

        self.domain_edit.setText(_translate("MainWindow", "http://"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.authorization_tab), _translate("MainWindow",
                                                                                             "Authorization"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.general_tab), _translate("MainWindow", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.workmode_tab), _translate("MainWindow", "WorkMode"))

        self.hot_key_mode_radiobutton.setText(_translate("MainWindow", "hot key mode"))
        self.keyword_replace_mode_radiobutton.setText(_translate("MainWindow", "Key word replace mode"))

        self.check_button.setText(_translate("MainWindow", "Authenticate"))
        self.reset_button.setText(_translate("MainWindow", "Reset"))
        self.save_button.setText(_translate("MainWindow", "Save"))


if __name__ == '__main__':
    app = QApplication([])
    option_window = OptionWindow()
    option_window.show()
    sys.exit(app.exec_())
