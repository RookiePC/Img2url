from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget


class QtPopComponent:
    """
    Do not instantiate this class alone
    """

    @QtCore.pyqtSlot(str, str)
    def pop_notification(self, title: str, message: str):
        """
        for outer thread's signal call to display a notification window
        :param message: message to display in message box
        :param title: title for message box window
        :return: None
        """
        self.pop_window(title, message, QMessageBox.Information)

    @QtCore.pyqtSlot(str, str)
    def pop_warning(self, title: str, message: str):
        """
        for outer thread's signal call to display a warning window
        :param message: message to display in message box
        :param title: title for message box window
        :return: None
        """
        self.pop_window(title, message, QMessageBox.Warning)

    @QtCore.pyqtSlot(str, str)
    def pop_error(self, title: str, message: str):
        """
        for outer thread's sinal call to display a error window
        :param message: message to display in message box
        :param title: title for message box window
        :return: None
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
        pop = QMessageBox(self)
        pop.setIcon(icon)
        pop.setWindowTitle(title)
        pop.move(QDesktopWidget().availableGeometry().center())
        pop.setText(message)
        pop.exec_()
