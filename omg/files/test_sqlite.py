from datetime import datetime

import pytest
from taglib import Path

from omg.files import FileInfo
from omg.files.sqlite import SqliteAudioFileDatabase


@pytest.fixture
def memory_db():
    db = SqliteAudioFileDatabase(':memory:')
    db.init()
    return db


def test_get_files_empty_initially(memory_db):
    assert len(list(memory_db.get_files())) == 0


def test_add_single_file(memory_db):
    info = FileInfo(path=Path('/a/test.mp3'), mtime=datetime(2023, 9, 25, 16, 19))
    tags = {'title': ['some title'], 'artist': ['some artist']}
    memory_db.add_or_update(info, tags)
    assert len(list(memory_db.get_files())) == 1
    tags_from_db = memory_db.get_tags(info.path)
    assert tags_from_db == tags


def test_add_file_no_tags(memory_db):
    info = FileInfo(path=Path('/test.flac'), mtime=datetime.utcnow())
    memory_db.add_or_update(info, tags={})
    tags_from_db = memory_db.get_tags(info.path)
    assert tags_from_db == {}


def test_get_tags_not_existing_file(memory_db):
    tags_from_db = memory_db.get_tags(Path('/no.ogg'))
    assert tags_from_db is None


def test_add_file_then_update(memory_db):
    info = FileInfo(path=Path('/a/test.mp3'), mtime=datetime(2023, 9, 25, 16, 19))
    tags_1 = {'title': ['some title'], 'artist': ['some artist']}
    memory_db.add_or_update(info, tags_1)
    tags_2 = {'title': ['another title'], 'album': ['some album']}
    memory_db.add_or_update(info, tags_2)
    assert len(list(memory_db.get_files())) == 1
    assert memory_db.get_tags(info.path) == tags_2


def test_remove(memory_db):
    info_1 = FileInfo(path=Path('/file.flac'), mtime=datetime.utcnow())
    tags_1 = {'artist': ['Bob Dylan']}
    info_2 = FileInfo(path=Path('/file_2.flac'), mtime=datetime.utcnow())
    tags_2 = {'artist': ['John Coltrane']}
    memory_db.add_or_update(info_1, tags_1)
    memory_db.add_or_update(info_2, tags_2)
    assert memory_db.get_tags(info_1.path) == tags_1

    memory_db.remove_file(info_1.path)
    assert memory_db.get_tags(info_1.path) is None
    assert memory_db.get_tags(info_2.path) == tags_2
    assert len(list(memory_db.get_files())) == 1
