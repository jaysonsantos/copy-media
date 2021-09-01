from datetime import datetime
from pathlib import Path


def test_copy_movie_without_year(processor):
    processor, config, base, destination = processor
    assert list(destination.rglob("*")) == []
    assert processor.process() == 1
    base_files = list(base.rglob("*"))
    assert len(base_files) == 1
    assert base_files[0].name == "The Incredible Hulk.mkv"
    assert (destination / "Movies").exists()
    assert (destination / "Movies" / "The Incredible Hulk").exists()
    assert (
        destination / "Movies" / "The Incredible Hulk" / "The Incredible Hulk.mkv"
    ).exists()


def test_copy_movie_with_year(processor):
    processor, config, base, destination = processor
    assert list(destination.rglob("*")) == []
    hulk = base / "The Incredible Hulk.mkv"
    hulk.rename(hulk.parent / "The Incredible Hulk (2008).mkv")
    assert processor.process() == 1
    assert (destination / "Movies").exists()
    assert (destination / "Movies" / "The Incredible Hulk (2008)").exists()
    assert (
        destination
        / "Movies"
        / "The Incredible Hulk (2008)"
        / "The Incredible Hulk (2008).mkv"
    ).exists()


def test_copy_movie_full_name(processor):
    processor, config, base, destination = processor
    assert list(destination.rglob("*")) == []
    hulk = base / "The Incredible Hulk.mkv"
    hulk.rename(
        hulk.parent / "The.Incredible.Hulk.2008.2160p.UHD.BluRay.X265-IAMABLE.mkv"
    )
    assert processor.process() == 1
    assert (destination / "Movies").exists()
    assert (destination / "Movies" / "The Incredible Hulk (2008)").exists()
    assert (
        destination
        / "Movies"
        / "The Incredible Hulk (2008)"
        / "The.Incredible.Hulk.2008.2160p.UHD.BluRay.X265-IAMABLE.mkv"
    ).exists()


def test_copy_old_files(processor):
    processor, config, base, destination = processor
    processor.last_run = datetime.now().timestamp()
    assert processor.process() == 0
    base_files = list(base.rglob("*"))
    assert len(base_files) == 1
    destination_files = list(destination.rglob("*"))
    assert not destination_files


def test_copy_nested_directory(processor):
    processor, config, base, destination = processor
    assert list(destination.rglob("*")) == []
    hulk: Path = base / "The Incredible Hulk.mkv"
    nested = hulk.parent / "The Incredible Hulk"
    nested.mkdir()

    hulk.rename(nested / hulk.name)
    assert processor.process() == 1
    assert (destination / "Movies").exists()
    assert (destination / "Movies" / "The Incredible Hulk").exists()
    assert (
        destination / "Movies" / "The Incredible Hulk" / "The Incredible Hulk.mkv"
    ).exists()


def test_copy_existing_file_same_size(processor):
    processor, config, base, destination = processor

    assert processor.process() == 1
    expected_file = (
        destination / "Movies" / "The Incredible Hulk" / "The Incredible Hulk.mkv"
    )
    assert expected_file.exists()
    creation_date = expected_file.stat().st_ctime
    assert processor.process() == 1
    assert creation_date == expected_file.stat().st_ctime


def test_copy_existing_file_different_size(processor):
    processor, config, base, destination = processor

    assert processor.process() == 1
    expected_file = (
        destination / "Movies" / "The Incredible Hulk" / "The Incredible Hulk.mkv"
    )
    assert expected_file.exists()
    creation_date = expected_file.stat().st_ctime
    expected_file.write_text("new_file")
    assert processor.process() == 1
    assert creation_date != expected_file.stat().st_ctime
    # It should go back to its original value
    assert expected_file.read_text() == ""
