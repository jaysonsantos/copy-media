__version__ = "0.1.0"

import os
from contextlib import contextmanager
from pathlib import Path

from loguru import logger

CONFIG_DIR = Path(os.environ.get("CONFIG_DIR", "~/.config/copy-media")).expanduser()
LOCK_FILE = CONFIG_DIR / "copy-media.lock"
LAST_PROCESSED_FILES = CONFIG_DIR / "last-time"
LOG_FILE = CONFIG_DIR / "log.txt"

logger.add(LOG_FILE, rotation="5 days", diagnose=True, backtrace=True, level="INFO")


@contextmanager
def lock():
    """
    >>> ctx = lock()
    >>> ctx.__enter__()  # doctest: +ELLIPSIS
    PosixPath('.../copy-media.lock')
    >>> lock().__enter__()
    Traceback (most recent call last):
    ...
    SystemExit: 1
    >>> del ctx  # Make its context go exit
    >>> lock().__enter__()  # doctest: +ELLIPSIS
    PosixPath('.../copy-media.lock')
    """
    if LOCK_FILE.exists():
        logger.error("already running")
        exit(1)

    LOCK_FILE.write_text("locked")
    try:
        yield LOCK_FILE
    finally:
        logger.debug("deleting lock")
        LOCK_FILE.unlink()
