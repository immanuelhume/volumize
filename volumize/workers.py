import os
import random
import shutil
import zipfile
from pathlib import Path
from typing import List

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot


class ToCbzWorker(QRunnable):

    def __init__(self, chapters: List[Path], destination: Path):
        super().__init__()
        self.folders = chapters
        self.destination = destination
        self.signals = ToCbzWorkerSignals()

    @pyqtSlot()
    def run(self):
        to_cbz(self.folders, self.destination, self.signals)


class ToCbzWorkerSignals(QObject):

    completed = pyqtSignal(str)
    progress = pyqtSignal(int)
    preparing = pyqtSignal(bool, str)


# BUG the loading bar sucks
def to_cbz(chapters: List[Path],
           dest: Path,
           signals: ToCbzWorkerSignals = None):

    prep_messages = [
        'running for student council...',
        'entering isekai...',
    ]

    signals.preparing.emit(True, random.choice(prep_messages))

    cbz_file = zipfile.ZipFile(dest, 'w')
    pages = []
    tmp_folder = dest.parent / 'tmp'
    os.mkdir(tmp_folder)
    os.chdir(tmp_folder)

    for n, chapter in enumerate(chapters):
        if chapter.is_dir():
            pages.extend([(chapter.name, file)
                          for file in os.scandir(chapter)])
        else:
            # extract file contents first
            with zipfile.ZipFile(chapter, 'r') as zf:
                zf.extractall(tmp_folder)
            pages.extend([(chapter.stem, file)
                          for file in os.scandir(tmp_folder / chapter.stem)])

    signals.preparing.emit(False, '')

    total_n = len(pages)
    for n, (chapter, page) in enumerate(pages):
        cbz_file.write(page, Path(chapter) / page.name)
        if signals:
            signals.progress.emit(int((100 * n) / total_n))
    cbz_file.close()
    if signals:
        signals.completed.emit(f'{dest} created!')
    shutil.rmtree(tmp_folder)
