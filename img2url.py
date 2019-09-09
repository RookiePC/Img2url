from PySide2 import QtWidgets
from Image_uploader import ImageUploader
from first_attempt import FloatingWidget
from Option_control import OptionControl


class Img2url:
    def __init__(self):
        self.app = QtWidgets.QApplication([])

        self.main_window = FloatingWidget(self.app.primaryScreen())
        self.image_uploader = ImageUploader()
        self.option_control = OptionControl(self.image_uploader.option_data)
