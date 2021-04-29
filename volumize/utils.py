import os
import re
import zipfile
from pathlib import Path
from typing import List


def natural_sort_key(s: str, _nsre=re.compile('([0-9]+)')) -> List:
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]


def to_cbz(chapters: List['Path'],
           dest: 'Path',
           signals: 'ToCbzWorkerSignals' = None):
    cbz_file = zipfile.ZipFile(dest, 'w')
    pages = [(folder.name, file) for folder in chapters
             for file in os.scandir(folder)]
    total_n = len(pages)
    for n, (chapter, page) in enumerate(pages):
        cbz_file.write(page, Path(chapter) / page.name)
        if signals:
            signals.progress.emit(int(100 * n) / total_n)
    cbz_file.close()
    if signals:
        signals.completed.emit(f'{dest} created!')
