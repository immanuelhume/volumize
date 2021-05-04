import re
from typing import List

# TODO remove the weird loading bar and add cool text instead

valid_input_file_formats = ['.zip', '.cbz']


def natural_sort_key(s: str, _nsre=re.compile('([0-9]+)')) -> List:
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]
