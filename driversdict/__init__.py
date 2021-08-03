from pathlib import Path
import locale

DATAHOME: str = (Path.home() / ".local" / "share" / "driversdict").as_posix()
DICTIONARY: str = (Path(DATAHOME) / "dictionary.txt").as_posix()
DATABASE: str = (Path(DATAHOME) / "driversdict.sqlite").as_posix()
SHELL_ENCODING = None

def shell_encoding():
    global SHELL_ENCODING
    if SHELL_ENCODING is None:
        SHELL_ENCODING = locale.getdefaultlocale()[1]
    return SHELL_ENCODING