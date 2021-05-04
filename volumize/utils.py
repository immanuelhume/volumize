import os
import re
import shutil
import zipfile
from pathlib import Path
from typing import List

from .workers import ToCbzWorkerSignals

# TODO remove the weird loading bar and add cool text instead

valid_input_file_formats = ['.zip', '.cbz']


def natural_sort_key(s: str, _nsre=re.compile('([0-9]+)')) -> List:
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]


# BUG the loading bar sucks
def to_cbz(chapters: List[Path],
           dest: Path,
           signals: ToCbzWorkerSignals = None):
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

    total_n = len(pages)
    for n, (chapter, page) in enumerate(pages):
        cbz_file.write(page, Path(chapter) / page.name)
        if signals:
            signals.progress.emit(int((100 * n) / total_n))
    cbz_file.close()
    if signals:
        signals.completed.emit(f'{dest} created!')
    shutil.rmtree(tmp_folder)
