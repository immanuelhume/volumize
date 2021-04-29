# TODO drag and drop into file list view
# TODO open file explorer upon completion option
# TODO implement reverse engineering - unpack


import os
import re
import zipfile
from pathlib import Path
from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .MainWindow import Ui_MainWindow
from .utils import natural_sort_key, to_cbz


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super().__init__()
        self.setupUi(self)
        self.show()
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
        self.toggle_enabled(self.intially_locked_widgets)
        self.lineEdit_inputFolder.textChanged.connect(self.enable_all)

        self.pushButton_inputFolder.clicked.connect(self.select_input_folder)
        self.pushButton_outputFolder.clicked.connect(self.select_output_folder)

        self.files_model = FilesModel()
        self.listView_chapters.setModel(self.files_model)

        self.pushButton_compile.clicked.connect(self.handle_compile)

    @staticmethod
    def toggle_enabled(widgets: List):
        for widget in widgets:
            widget.setEnabled(not widget.isEnabled())

    def enable_all(self):
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
            self.display_selection(input_folder)

    def display_selection(self, input_folder: 'Path'):
        self.lineEdit_inputFolder.setText(input_folder)
        self.lineEdit_outputFolder.setText(input_folder)
        self.lineEdit_mangaTitle.setText(Path(input_folder).name)

        self.files_model.dirname = Path(input_folder)
        chapters = [item for item in os.listdir(input_folder) if
                    os.path.isdir(Path(input_folder) / item)]
        self.files_model.files = sorted(chapters, key=natural_sort_key)
        self.files_model.layoutChanged.emit()

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


class ToCbzWorkerSignals(QObject):

    completed = pyqtSignal(str)
    progress = pyqtSignal(int)


class ToCbzWorker(QRunnable):

    def __init__(self, folders: List['Path'], destination: 'Path'):
        super().__init__()
        self.folders = folders
        self.destination = destination
        self.signals = ToCbzWorkerSignals()

    @pyqtSlot()
    def run(self):
        to_cbz(self.folders, self.destination, self.signals)


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
    app.exec_()
