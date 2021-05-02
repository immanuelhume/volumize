import os

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QListView


class DropListView(QListView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.signals = DropListViewSignals()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()

            # validate
            files = [str(url.toLocalFile()) for url in e.mimeData().urls()]
            if len(files) > 1:
                self.signals.error.emit('Please drop only one folder at a time!')
            elif not os.path.isdir(files[0]):
                self.signals.error.emit('Please drop folders only!')
            else:
                self.signals.dropped.emit(files[0])


class DropListViewSignals(QObject):

    dropped = pyqtSignal(str)
    error = pyqtSignal(str)
