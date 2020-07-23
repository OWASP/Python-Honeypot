import json
from core.compatible import version

def __log_into_file(filename, mode, data):
    """
    write a content into a file (support unicode).
    Args:
        filename: the filename
        mode: writing mode (a, ab, w, wb, etc.)
        data: content
        language: language
    Returns:
        True if success otherwise None
    """
    log = ''
    if version() == 2:
        if isinstance(data, str):
            try:
                log = json.loads(data)
            except ValueError:
                log = ''

        with open(filename, mode) as save:
            save.write(data + '\n')
    else:
        if isinstance(data, str):
            try:
                log = json.loads(data)
            except ValueError:
                log = ''


        with open(filename, mode, encoding='utf-8') as save:
            save.write(data + '\n')
    return True
