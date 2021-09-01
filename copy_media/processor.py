import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Tuple

from guessit import guessit
from loguru import logger


@dataclass
class Processor:
    base_directory: Path
    destination_directory: Path
    # keys can be episode or movie
    mapping: Dict[str, str]
    last_run: int

    def process(self) -> int:
        entries = list(self.fetch_entries())
        self.copy(zip(entries, self.parse_entries(entries)))
        return len(entries)

    def fetch_entries(self):
        for name in self.base_directory.glob("*"):
            stat = name.stat()
            logger.debug(
                f"{stat.st_ctime} >= {self.last_run} = {stat.st_ctime >= self.last_run}"
            )
            if stat.st_ctime >= self.last_run:
                yield name

    @staticmethod
    def parse_entries(entries: List[Path]):
        """
        >>> from pathlib import Path
        >>> entry, = Processor.parse_entries([Path("doctor who 2005 s03e01 YTS.mkv")])
        >>> entry['title']
        'doctor who'
        >>> entry['year']
        2005
        >>> entry['season']
        3
        >>> entry['episode']
        1
        >>> entry['type']
        'episode'
        """
        return [guessit(entry.name) for entry in entries]

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
        if source.is_dir():
            final_destination = folder
        else:
            final_destination = folder / source.name
        self._copy(source, final_destination)

    def _copy(self, source: Path, destination: Path):
        if source.is_dir():
            for child in source.iterdir():
                self._copy(child, destination / child.name)

            return

        logger.info(f"copying {source} to {destination}")
        if not self._should_copy(source, destination):
            logger.debug(f"skippig copying {source}")
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source, destination)

    def _should_copy(self, source: Path, destination: Path):
        return not (
            destination.exists() and source.stat().st_size == destination.stat().st_size
        )
