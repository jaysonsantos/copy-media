import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, Tuple

from guessit import guessit
from loguru import logger


@dataclass
class Processor:
    base_directory: Path
    destination_directory: Path
    # keys can be episode or movie
    mapping: Dict[str, str]
    last_run: int

    def process(self):
        entries = list(self.fetch_entries())
        self.copy(zip(entries, self.parse_entries(entries)))

    def fetch_entries(self):
        for name in self.base_directory.glob("*"):
            stat = name.stat()
            logger.debug(
                f"{stat.st_ctime} >= {self.last_run} = {stat.st_ctime >= self.last_run}"
            )
            if stat.st_ctime >= self.last_run:
                yield name

    @staticmethod
    def parse_entries(entries):
        return [guessit(entry) for entry in entries]

    def copy(self, entries: Iterator[Tuple[Path, Dict[str, str]]]):
        for entry in entries:
            self.copy_entry(entry)

    def copy_entry(self, entry: Tuple[Path, Dict[str, str]]):
        source, data = entry
        folder_name = f"{data['title']}"
        if "year" in data:
            folder_name += f" ({data['year']})"
        folder = self.destination_directory / self.mapping[data["type"]] / folder_name
        folder.mkdir(parents=True, exist_ok=True)
        final_destination = folder / source.name
        logger.info(f"copying {source} to {final_destination}")
        if source.is_dir():
            shutil.copytree(source, final_destination, dirs_exist_ok=True)
        else:
            shutil.copy(source, final_destination)
