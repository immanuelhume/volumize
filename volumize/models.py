from pathlib import Path

from PyQt5.QtCore import QAbstractListModel, Qt


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
