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
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from Views import MigratorWindow, ProgressDialog
from Tools import ImageUploader, ImageMigrator


class MigratorControl(QObject):
    warning_signal = pyqtSignal(str, str)
    error_signal = pyqtSignal(str, str)
    notify_signal = pyqtSignal(str, str)

    def __init__(self, uploader: ImageUploader.ImageUploader):
        super().__init__()
        self.image_migrator = ImageMigrator.ImageMigrator(uploader)
        self.migrator_window = MigratorWindow.MigratorWindow()
        self.progress_dialog = ProgressDialog.ProgressDialogView()

        self.warning_signal.connect(self.migrator_window.pop_warning)
        self.error_signal.connect(self.migrator_window.pop_error)
        self.notify_signal.connect(self.migrator_window.pop_notification)

        # the respond to the submenu click is show the window
        self.on_migrate_from_file_clicked = self.migrator_window.show

        self.migrator_window.migrate_button.clicked.connect(self.on_migrate_button_in_migrate_window_clicked)

        self.migrate_task = None

    def on_migrate_from_clipboard_clicked(self):
        self.progress_dialog.reset()
        self.progress_dialog.show()
        self.progress_dialog.play_thread.start()
        self.migrate_task = MigrateFromClipboardTask(self)
        self.migrate_task.start()

    def on_migrate_button_in_migrate_window_clicked(self):
        self.progress_dialog.reset()
        self.progress_dialog.show()
        self.progress_dialog.play_thread.start()
        self.migrate_task = MigrateFromFileTask(self)
        self.migrate_task.start()


class BaseTask(QThread):
    close_dialog_signal = pyqtSignal()

    def __init__(self, migrator_control: MigratorControl):
        super().__init__()
        self.progress_dialog = migrator_control.progress_dialog
        self.progress_dialog.close_callback = self.terminate
        self.migrator_control = migrator_control
        self.error_signal = self.migrator_control.error_signal
        self.warning_signal = self.migrator_control.warning_signal
        self.notify_signal = self.migrator_control.notify_signal
        self.image_migrator = self.migrator_control.image_migrator
        self.migrator_window = self.migrator_control.migrator_window

        self.close_dialog_signal.connect(self.progress_dialog.force_close)


class MigrateFromFileTask(BaseTask):
    def __init__(self, migrator_control: MigratorControl):
        super().__init__(migrator_control)

    def run(self) -> None:
        self.image_migrator.init_statistics()

        try:
            new_file_path = self.image_migrator.migrate_from_file(self.migrator_window.md_file_path_line_edit.text(),
                                                                  self.migrator_window.dir_path_line_edit.text())
        except Exception as Ex:
            self.close_dialog_signal.emit()
            self.error_signal.emit('Migration from File Failed', Ex.__str__())
            return

        if not self.image_migrator.encountered_any_error():
            self.close_dialog_signal.emit()
            self.notify_signal.emit('Migration succeed',
                                    'Migration Succeed, {succeed_num} has been migrated. The new Markdown file'
                                    ' is saved as {new_path}'
                                    .format(succeed_num=self.image_migrator.migrate_succeed_num,
                                            new_path=new_file_path))
            return

        log_file_path = None

        try:
            log_file_path = self.image_migrator.save_errors_to_local_log_file()
        except Exception as ex:
            self.error_signal.emit('Log error failed', ex.__str__())

        if log_file_path is None:
            log_relevant_msg = 'failed to generate log.'
        else:
            log_relevant_msg = 'a log file has been saved to {log_path}, please check'.format(log_path=log_file_path)

        self.close_dialog_signal.emit()

        if self.image_migrator.failed_every_link_migration():
            self.error_signal.emit('Migrate from file failed',
                                   'Failed on each link\'s Migration, ' + log_relevant_msg)
        else:
            self.warning_signal.emit('Migration Partially Succeed',
                                     'Part({succeed_num} of all images({all_num} migrated successfully, '
                                     .format(succeed_num=self.image_migrator.migrate_succeed_num,
                                             all_num=self.image_migrator.total_image_num) + log_relevant_msg)


class MigrateFromClipboardTask(BaseTask):
    def run(self) -> None:
        # inits the statistics
        self.image_migrator.init_statistics()

        try:
            self.image_migrator.migrate_from_clipboard()
        except Exception as ex:
            self.close_dialog_signal.emit()
            self.error_signal.emit('Migrate from clipboard failed',
                                   'Failed to migrate data in clipboard, beacause :\n' + ex.__str__())
            return

        if self.image_migrator.total_image_num == 0:
            self.close_dialog_signal.emit()
            self.warning_signal.emit('Noting migrated',
                                     'No valid link found in clipboard, please check.')
            return

        if not self.image_migrator.encountered_any_error():
            self.close_dialog_signal.emit()
            self.notify_signal.emit('Migration succeed',
                                    'Migration Succeed, {succeed_num} has been migrated. The new content is copied '
                                    'to clipboard. '
                                    .format(succeed_num=self.image_migrator.migrate_succeed_num))
            return

        log_file_path = None

        try:
            log_file_path = self.image_migrator.save_errors_to_local_log_file()
        except Exception as ex:
            self.error_signal.emit('Log error failed', ex.__str__())

        if log_file_path is None:
            log_relevant_msg = 'failed to generate log.'
        else:
            log_relevant_msg = 'a log file has been saved to {log_path}, please check'.format(log_path=log_file_path)

        self.close_dialog_signal.emit()

        if self.image_migrator.failed_every_link_migration():
            self.error_signal.emit('Migrate from clipboard failed',
                                   'Failed on each link\'s Migration, ' + log_relevant_msg)
        else:
            self.warning_signal.emit('Migration Partially Succeed',
                                     'Part({succeed_num} of all images({all_num} migrated successfully, '
                                     .format(succeed_num=self.image_migrator.migrate_succeed_num,
                                             all_num=self.image_migrator.total_image_num) + log_relevant_msg)
