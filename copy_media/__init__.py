__version__ = "0.1.0"

from contextlib import contextmanager
from pathlib import Path

from loguru import logger

CONFIG_DIR = Path("~/.config/copy-media").expanduser()
LOCK_FILE = CONFIG_DIR / "copy-media.lock"
LAST_TIME_RUN = CONFIG_DIR / "last-time"
LOG_FILE = CONFIG_DIR / "log.txt"

logger.add(LOG_FILE, rotation="5 days", diagnose=True, backtrace=True, level="INFO")


@contextmanager
def lock():
    if LOCK_FILE.exists():
        logger.error("already running")
        exit(1)

    LOCK_FILE.write_text("locked")
    try:
        yield LOCK_FILE
    finally:
        logger.debug("deleting lock")
        LOCK_FILE.unlink()
