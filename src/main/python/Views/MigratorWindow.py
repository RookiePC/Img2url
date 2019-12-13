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
from Views import QtPopComponent
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog


class MigratorWindow(QMainWindow, QtPopComponent.QtPopComponent):
    def __init__(self):
        super().__init__()
        self.setObjectName("Migrator_main")
        self.setFixedSize(340, 200)

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("Migrate_method_choice")

        self.gridLayoutWidget = QtWidgets.QWidget(self.central_widget)

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()

        self.md_file_path_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.md_browse_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.md_browse_button.clicked.connect(self.on_file_borwse_button_clicked)

        self.MD_file_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Dir_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.dir_path_line_edit = QtWidgets.QLineEdit(self.gridLayoutWidget)

        self.dir_browse_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.dir_browse_button.clicked.connect(self.on_save_dir_browse_button_clicked)

        self.migrate_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.setupUi()

    def setupUi(self):
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 321, 197))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout.setContentsMargins(0, 5, 0, 5)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")

        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.md_file_path_line_edit.setReadOnly(True)

        self.md_file_path_line_edit.setObjectName("md_file_path_line_edit")
        self.horizontalLayout_2.addWidget(self.md_file_path_line_edit)

        self.md_browse_button.setObjectName("md_browse_button")
        self.horizontalLayout_2.addWidget(self.md_browse_button)

        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.horizontalLayout.setContentsMargins(3, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.MD_file_label.setTextFormat(QtCore.Qt.PlainText)
        self.MD_file_label.setObjectName("MD_file_label")
        self.horizontalLayout.addWidget(self.MD_file_label)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.dir_path_line_edit.setReadOnly(True)
        self.dir_path_line_edit.setObjectName("dir_path_line_edit")
        self.horizontalLayout_4.addWidget(self.dir_path_line_edit)

        self.dir_browse_button.setEnabled(True)
        self.dir_browse_button.setObjectName("dir_browse_button")
        self.horizontalLayout_4.addWidget(self.dir_browse_button)
        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)

        self.horizontalLayout_3.setContentsMargins(3, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.Dir_label.setObjectName("Dir_label")
        self.horizontalLayout_3.addWidget(self.Dir_label)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)

        self.migrate_button.setObjectName("migrate_button")
        self.horizontalLayout_5.addWidget(self.migrate_button)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
        self.setCentralWidget(self.central_widget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Migrator_main", "Migrator"))
        self.setStatusTip(_translate("Migrator_main", "Help migrates the images in markdown file"))
        self.md_browse_button.setText(_translate("Migrator_main", "Browse"))
        self.MD_file_label.setText(_translate("Migrator_main", "MD File to Migrate"))
        self.dir_browse_button.setText(_translate("Migrator_main", "Browse"))
        self.Dir_label.setText(_translate("Migrator_main", "Dircectory to save result"))
        self.migrate_button.setText(_translate("Migrator_main", "Migrate"))

    def on_save_dir_browse_button_clicked(self):
        save_path: str = str(QFileDialog.getExistingDirectory(self, "Select Directory To Store Results"))
        if save_path is not None and len(save_path) != 0:
            self.dir_path_line_edit.setText(save_path)

    def on_file_borwse_button_clicked(self):
        file_path: str = QFileDialog.getOpenFileName(self, caption='Select Target Markdown File', filter=('Markdown file (*.md *.MD *.markdown'))[0]
        if file_path is not None and len(file_path) != 0:
            self.md_file_path_line_edit.setText(file_path)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication([])
    migrator_window = MigratorWindow()
    migrator_window.show()
    sys.exit(app.exec_())