# TODO drag and drop into file list view
# TODO open file explorer upon completion option
# TODO disable all fields except select folder

import os
import re
import zipfile
from pathlib import Path
from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .MainWindow import Ui_MainWindow


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]


def toggle_enabled(*widgets):
    for widget in widgets:
        widget.setEnabled(not widget.isEnabled())


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super().__init__()
        self.setupUi(self)
        self.show()

        # disable everything except select folder
        toggle_enabled(
            self.label_3,
            self.lineEdit_outputFolder,
            self.pushButton_outputFolder,
            self.label_4,
            self.lineEdit_mangaTitle,
            self.checkBox_showFiles,
            self.label,
            self.doubleSpinBox_volumeNo,
            self.listView_chapters,
            self.pushButton_compile,
            self.progressBar
        )

        self.threadpool = QThreadPool()

        self.pushButton_inputFolder.clicked.connect(self.select_input_folder)
        self.pushButton_outputFolder.clicked.connect(self.select_output_folder)

        self.files_model = FilesModel()
        self.listView_chapters.setModel(self.files_model)

        self.pushButton_compile.clicked.connect(self.handle_compile)

    def select_input_folder(self):
        dir_to_open = self.lineEdit_inputFolder.text() or str(Path.home())
        input_folder = QFileDialog.getExistingDirectory(
            self, 'Select folder', dir_to_open)
        if input_folder:
            self.lineEdit_inputFolder.setText(input_folder)
            self.lineEdit_outputFolder.setText(input_folder)
            self.lineEdit_mangaTitle.setText(Path(input_folder).name)

            self.files_model.dirname = Path(input_folder)
            self.files_model.files = sorted(os.listdir(
                input_folder), key=natural_sort_key)
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

    def one_volume_done(self):
        self.progressBar.reset()
        self.doubleSpinBox_volumeNo.setValue(
            self.doubleSpinBox_volumeNo.value() + 1)


class ToCbzWorkerSignals(QObject):

    completed = pyqtSignal()
    progress = pyqtSignal(int)


class ToCbzWorker(QRunnable):

    def __init__(self, folders: List['Path'], destination: 'Path'):
        super().__init__()
        self.folders = folders
        self.destination = destination
        self.signals = ToCbzWorkerSignals()

    @ pyqtSlot()
    def run(self):
        cbz_file = zipfile.ZipFile(self.destination, 'w')
        files = [(folder.name, file) for folder in self.folders
                 for file in os.scandir(folder)]
        total_n = len(files)
        for n, (chapter, page) in enumerate(files):
            self.signals.progress.emit(int((100 * n) / total_n))
            cbz_file.write(page, Path(chapter) / page.name)
        cbz_file.close()
        self.signals.completed.emit()


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


if __name__ == '__main__':
    pass
