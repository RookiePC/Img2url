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
import os
import sys
import enum
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QCoreApplication, QPoint
from PyQt5.QtGui import QPixmap, QImage, QCursor, QScreen, QIcon
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect, QMenu, QSystemTrayIcon, QMessageBox

import resource


class DisplayMode(enum.Enum):
    normal_no_hook = 0,
    normal_hook_installed = 1,
    ready_to_paste = 2,
    cant_work_normally = 3


class FloatingWidget(QtWidgets.QWidget):
    def __init__(self, screen: QScreen):
        super().__init__()
        print(os.getcwd())

        self.icon_resource_root = ':display/'

        # sets the name of all icon file
        self.NORMAL_ICO = self.icon_resource_root + 'favicon.ico'
        self.GRAY_ICO = self.icon_resource_root + 'favicon_gray.ico'
        self.BLUE_ICO = self.icon_resource_root + 'favicon_blue.ico'
        self.GREEN_ICO = self.icon_resource_root + 'favicon_green.ico'
        self.ORANGE_ICO = self.icon_resource_root + 'favicon_orange.ico'

        self.pix = QPixmap(QImage(self.GRAY_ICO))
        self.pos = None
        self.label = QLabel(self)
        self.layout = QtWidgets.QVBoxLayout()

        # stores the func instead of value
        # this will make it still works properly even if the resolution changed
        # (I wonder who would be so bored to do that to this little cute app）
        self.screen_size = screen.size

        self.menu_action_hide = None
        self.menu_action_options = None
        self.menu_action_quick_hook = None
        self.menu_action_unhook = None
        self.menu_action_quit = None
        self.context_menu = None
        self.init_context_menu()

        self.tray_icon = None
        self.init_tray_icon()

        self.init_ui()

    def init_ui(self):
        """
        initializes the ui elements in main window
        :return:
        """
        # resize this window to fit the innner image
        self.resize(self.pix.size())

        # set the window to frameless and keep it always on top
        self.setWindowFlags(Qt.WindowType.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setWindowFlags( Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # set the background invisible
        self.setAttribute(Qt.WA_TranslucentBackground)

        # sets this for MacOS (keep tool on top and hides the rocket icon)
        if sys.platform == 'darwin':
            self.setAttribute(Qt.WA_MacAlwaysShowToolWindow)
            import AppKit
            info = AppKit.NSBundle.mainBundle().infoDictionary()
            info["LSBackgroundOnly"] = "1"

        # now sets the image to label
        self.label.setPixmap(self.pix)

        # add that label into our main widget
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # sets the shadow effect around it
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

    def init_context_menu(self):
        """
        inits the context menu items
        :return: None
        """
        self.context_menu = QMenu()

        self.menu_action_options = self.context_menu.addAction('Options')
        self.menu_action_quick_hook = self.context_menu.addAction('Quick hook')
        self.menu_action_unhook = self.context_menu.addAction('Unhook')
        self.menu_action_hide = self.context_menu.addAction('Hide')
        menu_action_help = self.context_menu.addAction('Help')
        self.menu_action_quit = self.context_menu.addAction('Quit')

        self.menu_action_unhook.setEnabled(False)
        self.menu_action_quit.triggered.connect(self.context_menu_quit_clicked)
        menu_action_help.triggered.connect(self.context_menu_help_clicked)
        self.menu_action_hide.triggered.connect(self.context_menu_hide_clicked)

    def switch_display(self, mode: DisplayMode):
        """
        change the floating widgets appearance by resets the .icon file
        :param mode: determines the .icon to use
        :return:None
        """
        if mode == DisplayMode.normal_no_hook:
            self.pix = QPixmap(QImage(self.GRAY_ICO))
        elif mode == DisplayMode.normal_hook_installed:
            self.pix = QPixmap(QImage(self.BLUE_ICO))
        elif mode == DisplayMode.ready_to_paste:
            self.pix = QPixmap(QImage(self.GREEN_ICO))
        else:
            self.pix = QPixmap(QImage(self.ORANGE_ICO))

        self.label.setPixmap(self.pix)

    def context_menu_quit_clicked(self):
        """
        does the job before quit.
        :param event:
        :return:
        """
        QCoreApplication.quit()

    def context_menu_help_clicked(self):
        """
        shows help as it supposed to do, not implemented yet( TODO: fill this function)
        :param event:
        :return: None
        """
        print('help clicked')

    def context_menu_hide_clicked(self):
        """
        respond to the hide context menu click event
        :param event: for the interface only, not actually used inside the method
        :return: None
        """
        if self.menu_action_hide.text() == 'hide':
            self.menu_action_hide.setText('show')
            self.hide()
        else:
            self.menu_action_hide.setText('hide')
            self.show()

    def init_tray_icon(self):
        """
        initialises the tray icon, called after the original context menu initialed.
        :return: None
        """
        self.tray_icon = QSystemTrayIcon(QIcon(self.NORMAL_ICO))
        self.tray_icon.show()
        self.tray_icon.setContextMenu(self.context_menu)
        # self.tray_icon.showMessage("test", "hello there!", QSystemTrayIcon.Information, 500)
        self.tray_icon.setToolTip('Still living')

    @QtCore.pyqtSlot(str, str)
    def pop_warning(self, title: str, message: str):
        """
        for outer thread's signal call to display a warning window
        :param message: message to display in message box
        :param title: title for message box window
        :return:
        """
        self.pop_window(title, message, QMessageBox.Warning)

    @QtCore.pyqtSlot(str, str)
    def pop_error(self, title: str, message: str):
        """
        for outer thread's sinal call to display a error window
        :param message: message to display in message box
        :param title: title for message box window
        :return:
        """
        self.pop_window(title, message, QMessageBox.Critical)

    def pop_window(self, title: str, message: str, icon: QMessageBox.Icon):
        """
        pop a message box with given parameters
        :param title:
        :param message:
        :param icon:
        :return:
        """
        pop = QMessageBox()
        pop.setIcon(icon)
        pop.setWindowTitle(title)
        pop.setText(message)
        pop.exec_()

    def show_tray_icon_message(self, title: str, message: str, time: int = 300):
        """
        pops message on tray icon with given parameters
        :param title:
        :param message:
        :param mode:
        :param time: default to 300 m-seconds
        :return: None
        """
        self.tray_icon.showMessage(title, message, time)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        self.context_menu.exec_(self.mapToGlobal(event.pos()))

    def mousePressEvent(self, event):
        event.accept()
        if event.button() == Qt.LeftButton:
            self.pos = event.pos()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.pos:
            self.setCursor(QCursor(Qt.OpenHandCursor))
            self.move(self.re_map_pos(event.pos() - self.pos))
        event.accept()

    def re_map_pos(self, pos: QPoint) -> QPoint:
        """
        re map the position of the app, to prevent dragging it to outer space
        :param pos: a QPoint that app would move to
        :return: a position that always in window space
        """

        # calculates the screen's width and height and minus that of our floating window
        width = self.screen_size().width() - self.width()
        height = self.screen_size().height() - self.height()

        # map it to global position---the desktop position
        pos = self.mapToGlobal(pos)

        # set it back on border if it's out
        if pos.x() > width:
            pos.setX(width)
        elif pos.x() < 0:
            pos.setX(0)

        if pos.y() > height:
            pos.setY(height)
        elif pos.y() < 0:
            pos.setY(0)

        return pos

    def mouseReleaseEvent(self, event):
        self.pos = None
        self.setCursor(QCursor(Qt.ArrowCursor))
        event.accept()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Escape:
            QCoreApplication.quit()


# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#
#     widget = FloatingWidget(app.primaryScreen())
#     widget.show()
#
#     sys.exit(app.exec_())
