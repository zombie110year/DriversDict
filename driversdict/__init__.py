from pathlib import Path
import locale

DICTIONARY = (Path.home() / ".local" / "share" / "driversdict" / "dictionary.txt").as_posix()
SHELL_ENCODING = None

def shell_encoding():
    global SHELL_ENCODING
    if SHELL_ENCODING is None:
        SHELL_ENCODING = locale.getdefaultlocale()[1]
    return SHELL_ENCODING