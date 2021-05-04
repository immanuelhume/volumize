# TODO drag and drop into file list view
# TODO open file explorer upon completion option


import os
from pathlib import Path

from PyQt5 import Qt
from PyQt5.QtCore import QAbstractListModel, QThreadPool
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow

from .MainWindow import Ui_MainWindow
from .utils import natural_sort_key, valid_input_file_formats
from .workers import ToCbzWorker


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super().__init__()
        # uic.loadUi(f"{Path(__file__).parent / 'ui' / 'mainwindow.ui'}", self)
        self.setupUi(self)
        self.lineEdit_inputFolder.setFocus()
        self.threadpool = QThreadPool()

        self.intially_locked_widgets = [
            self.label_outputFolder,
            self.lineEdit_outputFolder,
            self.pushButton_outputFolder,
            self.label_mangaTitle,
            self.lineEdit_mangaTitle,
            self.checkBox_showFiles,
            self.label_volumeNo,
            self.doubleSpinBox_volumeNo,
            self.listView_chapters,
            self.pushButton_compile,
            self.progressBar
        ]

        # disable everything until a folder is selected
        # self.set_disabled()
        # self.lineEdit_inputFolder.textChanged.connect(self.set_enabled)

        self.listView_chapters.signals.dropped.\
            connect(self.display_folder_contents)
        self.listView_chapters.signals.error.connect(self.display_drop_errors)

        self.pushButton_inputFolder.clicked.connect(self.select_input_folder)
        self.pushButton_outputFolder.clicked.connect(self.select_output_folder)

        self.files_model = FilesModel()
        self.listView_chapters.setModel(self.files_model)

        self.pushButton_compile.clicked.connect(self.handle_compile)

    def set_disabled(self):
        for widget in self.intially_locked_widgets:
            widget.setEnabled(False)

    def set_enabled(self):
        # check if it's a valid path
        input_folder = self.lineEdit_inputFolder.text()
        if (os.path.isdir(input_folder)):
            for widget in self.intially_locked_widgets:
                widget.setEnabled(True)

    def select_input_folder(self):
        dir_to_open = self.lineEdit_inputFolder.text() or str(Path.home())
        input_folder = QFileDialog.getExistingDirectory(
            self, 'Select folder', dir_to_open)
        if input_folder:
            self.display_folder_contents(input_folder)

    def display_folder_contents(self, input_folder: 'Path'):
        self.lineEdit_inputFolder.setText(input_folder)
        self.lineEdit_outputFolder.setText(input_folder)
        self.lineEdit_mangaTitle.setText(Path(input_folder).name)

        self.files_model.dirname = Path(input_folder)
        chapters = [item.name for item in os.scandir(input_folder) if
                    item.is_dir() or
                    Path(item.path).suffix in valid_input_file_formats]
        self.files_model.files = sorted(chapters, key=natural_sort_key)
        self.files_model.layoutChanged.emit()

    def display_drop_errors(self, error_msg: str):
        self.statusBar.showMessage(error_msg)

    def select_output_folder(self):
        dir_to_open = self.lineEdit_outputFolder.text() or str(Path.home())
        output_folder = QFileDialog.getExistingDirectory(
            self, 'Select folder', dir_to_open)
        if output_folder:
            self.lineEdit_outputFolder.setText(output_folder)

    def handle_compile(self):
        selected = self.listView_chapters.selectedIndexes()
        self.listView_chapters.clearSelection()

        if selected:
            filenames = map(
                lambda index: self.files_model.files[index.row()],
                selected)
            filenames = [self.files_model.dirname / filename
                         for filename in set(filenames)]

            title = self.lineEdit_mangaTitle.text()
            volume_no = self.doubleSpinBox_volumeNo.cleanText().\
                rstrip('0').rstrip('.')
            archive_name = f'{title}, Vol. {volume_no}.cbz'

            destination = Path(self.lineEdit_outputFolder.text()) / archive_name

            toCbzWorker = ToCbzWorker(filenames, destination)
            toCbzWorker.signals.progress.connect(lambda i:
                                                 self.progressBar.setValue(i))
            toCbzWorker.signals.completed.connect(self.one_volume_done)
            self.threadpool.start(toCbzWorker)

    def one_volume_done(self, msg: str):
        self.statusBar.showMessage(msg)
        self.progressBar.reset()
        self.doubleSpinBox_volumeNo.setValue(
            self.doubleSpinBox_volumeNo.value() + 1)


class FilesModel(QAbstractListModel):

    dirname = Path()

    def __init__(self, files=None):
        super().__init__()
        self.files = files or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            filename = self.files[index.row()]
            return filename

    def rowCount(self, index):
        return len(self.files)


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
