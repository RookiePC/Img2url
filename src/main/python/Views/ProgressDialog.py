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

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
import time


class ProgressDialogView(QDialog):
    def __init__(self):
        super().__init__()
        self.setObjectName("progress_dialog")
        self.setFixedSize(340, 140)

        self.setWindowFlags(Qt.WindowTitleHint)

        self.gridLayoutWidget = QtWidgets.QWidget(self)

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)

        self.progress_bar = QtWidgets.QProgressBar(self.gridLayoutWidget)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.cancel_button = QtWidgets.QPushButton(self.gridLayoutWidget)

        self.content_label = QtWidgets.QLabel(self.gridLayoutWidget)

        self.init_ui()

        self.cancel_button.clicked.connect(self.close)

        self.play_thread = PlayProgressThread(self)

        self.close_callback = None
        self.force_quit = False

    def init_ui(self):
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 321, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.gridLayout.addWidget(self.progress_bar, 0, 0, 1, 1)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.content_label.setAlignment(QtCore.Qt.AlignCenter)
        self.content_label.setText("Preparing..")
        self.content_label.setObjectName("content_label")
        self.gridLayout.addWidget(self.content_label, 1, 0, 1, 1)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("progress_dialog", "Work in progress"))
        self.cancel_button.setText(_translate("progress_dialog", "Cancel"))
        # self.content_label.setText(_translate("progress_dialog", "TextLabel"))

    def set_progress_value(self, value: int):
        self.progress_bar.setValue(value)

    def set_text(self, text: str):
        self.content_label.setText(text)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:

        if not self.force_quit:
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if self.force_quit or reply == QMessageBox.Yes:
            self.play_thread.terminate()
            if not self.force_quit and self.close_callback is not None:
                self.close_callback()
            a0.accept()
        else:
            a0.ignore()

    def force_close(self):
        self.force_quit = True
        self.close()

    def reset(self):
        self.close_callback = None
        self.force_quit = False


class PlayProgressThread(QThread):
    progress_value_set_signal = pyqtSignal(int)
    text_set_signal = pyqtSignal(str)

    def __init__(self, dialog: ProgressDialogView):
        super().__init__()
        self.dialog = dialog

        self.progress_value_set_signal.connect(self.dialog.set_progress_value)
        self.text_set_signal.connect(self.dialog.set_text)

        self.meaningless_sentence = [
            'Reading the doc',
            'Trying to understand the content',
            'Is that a typo?',
            'Ummmm, give me a second',
            'Ok, What\'s next',
            'This one looks weird',
            'Finishing this paragraph',
            'Moving on to the next'
        ]

        self.sentence_num = len(self.meaningless_sentence)

    def run(self) -> None:
        cnt = 0
        text_index = 0
        text_to_display = self.meaningless_sentence[text_index]

        while True:
            cnt %= 100
            cnt += 1
            self.progress_value_set_signal.emit(cnt)

            if cnt % 8 == 0:
                text_to_display += '.'
                self.text_set_signal.emit(text_to_display)

            if cnt % 32 == 0:
                text_index += 1
                text_index %= self.sentence_num
                text_to_display = self.meaningless_sentence[text_index]

            time.sleep(0.1)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication([])
    dialog = ProgressDialogView()
    dialog.show()
    dialog.play_thread.start()
    sys.exit(app.exec_())
