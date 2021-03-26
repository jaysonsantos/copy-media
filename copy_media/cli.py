import time
from datetime import datetime
from pathlib import Path

import click
from loguru import logger

from copy_media import CONFIG_DIR, LAST_TIME_RUN, lock
from copy_media.processor import Processor


def validate_mapping(_, __, values):
    valid_mappings = {"episode", "movie"}
    for (key, value) in values:
        if key not in valid_mappings:
            raise ValueError(
                f"mappings must be any of {valid_mappings} and not {key!r}"
            )

    return values


@click.command()
@click.option(
    "--from",
    "from_",
    required=True,
    type=click.Path(True, file_okay=False, resolve_path=True),
)
@click.option(
    "--to",
    required=True,
    type=click.Path(True, file_okay=False, resolve_path=True, writable=True),
)
@click.option("--mapping", type=(str, str), callback=validate_mapping, multiple=True)
def main(from_, to, mapping):
    logger.debug("starting")
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().timestamp()
    last_time_run = float(LAST_TIME_RUN.read_text()) if LAST_TIME_RUN.exists() else 0
    logger.info(f"searching for files created after {last_time_run} in {from_}")
    with lock():
        processor = Processor(Path(from_), Path(to), dict(mapping), last_time_run)
        processor.process()
        LAST_TIME_RUN.write_text(str(now))
