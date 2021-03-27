from datetime import datetime


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
