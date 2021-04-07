# TODO drag and drop into file list view
# TODO open file explorer upon completion option

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .MainWindow import Ui_MainWindow

import os
from pathlib import Path
import re
import zipfile
from typing import List


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]


# class MainWindow(QMainWindow):

#     def __init__(self):
#         super().__init__()

#         # get icons
#         icons_dir = Path(__file__).parent.resolve() / 'icons'
#         icon_folder_plus = QIcon((str(icons_dir / 'folder--plus.png')))
#         icon_folder_open = QIcon((str(icons_dir / 'folder-open.png')))

#         self.setWindowTitle('Volumizer')
#         # self.setAttribute(Qt.WA_TranslucentBackground)

#         main_layout = QHBoxLayout()

#         # left half of window
#         main_left_layout = QVBoxLayout()

#         folder_selection_layout = QGridLayout()
#         label_input_folder = QLabel('Select folder:')
#         self.edit_input_folder = QLineEdit()
#         button_input_folder = QPushButton(icon_folder_plus, '')
#         label_output_folder = QLabel('Output folder:')
#         self.edit_output_folder = QLineEdit()
#         button_output_folder = QPushButton(icon_folder_open, '')
#         folder_selection_layout.addWidget(label_input_folder, 0, 0)
#         folder_selection_layout.addWidget(self.edit_input_folder, 0, 1, 1, 2)
#         folder_selection_layout.addWidget(button_input_folder, 0, 3)
#         folder_selection_layout.addWidget(label_output_folder, 1, 0)
#         folder_selection_layout.addWidget(self.edit_output_folder, 1, 1, 1, 2)
#         folder_selection_layout.addWidget(button_output_folder, 1, 3)

#         layout_manga_title = QHBoxLayout()
#         label_manga_title = QLabel('Manga title:')
#         self.edit_manga_title = QLineEdit()
#         layout_manga_title.addWidget(label_manga_title)
#         layout_manga_title.addWidget(self.edit_manga_title)

#         main_left_layout.addLayout(folder_selection_layout)
#         main_left_layout.addLayout(layout_manga_title)

#         # right half of window
#         main_right_layout = QVBoxLayout()

#         main_right_functions = QHBoxLayout()
#         label_volume_no = QLabel('Volume no.:')
#         self.spin_volume_no = QDoubleSpinBox()
#         self.spin_volume_no.setValue(1)
#         compile_button = QPushButton('Compile')
#         compile_button.clicked.connect(self.handle_compile)
#         main_right_functions.addWidget(label_volume_no)
#         main_right_functions.addWidget(self.spin_volume_no)
#         main_right_functions.addWidget(compile_button)

#         self.files_list = QListView()
#         self.files_list.setSelectionMode(3)
#         self.files_list_model = FilesModel()
#         self.files_list.setModel(self.files_list_model)

#         self.progressbar = QProgressBar()
#         self.progressbar.setFixedHeight(10)

#         main_right_layout.addLayout(main_right_functions)
#         main_right_layout.addWidget(self.files_list)
#         main_right_layout.addWidget(self.progressbar)

#         main_layout.addLayout(main_left_layout)
#         main_layout.addLayout(main_right_layout)

#         widget = QWidget()
#         widget.setLayout(main_layout)
#         self.setCentralWidget(widget)

#         self.show()

#         # the logics
#         self.threadpool = QThreadPool()

#         button_input_folder.clicked.connect(self.filedialog_input_folder)
#         button_output_folder.clicked.connect(self.filedialog_output_folder)

#     def filedialog_input_folder(self):
#         home_dir = str(Path.home())
#         dirname = QFileDialog.getExistingDirectory(self,
#                                                    'Select Folder',
#                                                    home_dir,)
#         if dirname:
#             self.files_list_model.dirname = Path(dirname)
#             self.display_files(dirname)
#             self.edit_input_folder.setText(dirname)
#             self.edit_output_folder.setText(dirname)
#             self.edit_manga_title.setText(self.files_list_model.dirname.name)

#     def filedialog_output_folder(self):
#         start_dir = self.edit_output_folder.text() or str(Path.home())
#         dirname = QFileDialog.getExistingDirectory(self,
#                                                    'Select Folder',
#                                                    start_dir,)
#         if dirname:
#             self.edit_output_folder.setText(dirname)

#     def display_files(self, dirname: 'Path'):
#         chapters = os.listdir(dirname)
#         chapters.sort(key=natural_sort_key)
#         self.files_list_model.files = chapters
#         self.files_list_model.layoutChanged.emit()

#     def handle_compile(self):
#         selected = self.files_list.selectedIndexes()
#         self.files_list.clearSelection()

#         if selected:
#             filenames = map(
#                 lambda index: self.files_list_model.files[index.row()],
#                 selected)
#             filenames = [self.files_list_model.dirname / filename
#                          for filename in set(filenames)]

#             title = self.edit_manga_title.text()
#             volume_no = self.spin_volume_no.cleanText().rstrip('0').rstrip('.')
#             archive_name = f'{title}, Vol. {volume_no}.cbz'

#             destination = Path(self.edit_output_folder.text()) / archive_name

#             toCbzWorker = ToCbzWorker(filenames, destination)
#             toCbzWorker.signals.progress.connect(lambda i:
#                                                  self.progressbar.setValue(i))
#             toCbzWorker.signals.completed.connect(self.one_volume_done)
#             self.threadpool.start(toCbzWorker)

#     def one_volume_done(self):
#         self.progressbar.reset()
#         self.spin_volume_no.setValue(self.spin_volume_no.value() + 1)

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super().__init__()
        self.setupUi(self)
        self.show()

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
