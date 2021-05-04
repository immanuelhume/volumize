from pathlib import Path
from typing import List

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

from .utils import to_cbz


class ToCbzWorkerSignals(QObject):

    completed = pyqtSignal(str)
    progress = pyqtSignal(int)


class ToCbzWorker(QRunnable):

    def __init__(self, chapters: List[Path], destination: Path):
        super().__init__()
        self.folders = chapters
        self.destination = destination
        self.signals = ToCbzWorkerSignals()

    @pyqtSlot()
    def run(self):
        to_cbz(self.folders, self.destination, self.signals)
