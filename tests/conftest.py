import os
from pathlib import Path

import pytest


@pytest.fixture
def processor(tmp_path: Path):
    config = tmp_path / "config"
    os.environ["CONFIG_DIR"] = str(config)
    from copy_media.processor import Processor

    base = tmp_path / "base"
    base.mkdir(parents=True)
    (base / "The Incredible Hulk.mkv").write_text("")
    destination = tmp_path / "destination"
    return (
        Processor(base, destination, {"movie": "Movies"}, 0),
        config,
        base,
        destination,
    )
