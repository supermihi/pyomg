import os
import sqlite3
from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path

from omg.files import FileInfo
from omg.files.tags import Tags, TagProvider


class TagDatabase(ABC):

    @abstractmethod
    def add_or_update(self, file: FileInfo, tags: Tags):
        raise NotImplementedError()

    @abstractmethod
    def get_files(self) -> Iterable[FileInfo]:
        raise NotImplementedError()

    @abstractmethod
    def remove_file(self, path: Path):
        raise NotImplementedError()


class SqliteAudioFileDatabase(TagProvider, TagDatabase):

    def __init__(self, db_path: os.PathLike | str):
        self.db_path = db_path
        self._connection = sqlite3.connect(db_path)

    def init(self):
        conn = self._connection
        conn.execute('''CREATE TABLE IF NOT EXISTS files(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            modification_time TIMESTAMP NOT NULL
            );''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS tags(
            file INTEGER NOT NULL,
            tag TEXT NOT NULL,
            value TEXT NOT NULL,
            FOREIGN KEY (file) REFERENCES files (id) ON DELETE CASCADE
                     );''')
        conn.execute('''
        CREATE INDEX IF NOT EXISTS tags_tag ON tags (tag);''')
        conn.commit()

    def add_or_update(self, file: FileInfo, tags: Tags):
        cursor = self._connection.cursor()
        cursor.execute('SELECT id, modification_time as "mtime [timestamp]" FROM files WHERE path=?',
                       (str(file.path),))
        ans = cursor.fetchone()
        if ans is None:
            cursor.execute('INSERT INTO files(path, modification_time) VALUES (?, ?)',
                           (str(file.path), file.mtime))
            file_id = cursor.lastrowid
            cursor.executemany('INSERT INTO tags(file, tag, value) VALUES(?, ?, ?)',
                               [(file_id, tag, value) for tag, values in tags.items() for value in values])
        else:
            file_id, mtime = ans
            cursor.execute('UPDATE files SET modification_time=? WHERE id=?', (mtime, file_id))
            cursor.execute('DELETE FROM tags WHERE file=?', (file_id,))
            cursor.executemany('INSERT INTO tags(file, tag, value) VALUES(?, ?, ?)',
                               [(file_id, tag, value) for tag, values in tags.items() for value in values])
        self._connection.commit()

    def remove_file(self, path: Path):
        with self._connection as c:
            c.execute('DELETE FROM files WHERE path = ?', (str(path),))

    def get_tags(self, path: Path) -> Tags | None:
        tags = {}
        result = self._connection.execute(
            'SELECT tag, value FROM files LEFT JOIN tags ON files.id = tags.file WHERE files.path = ?',
            (str(path),))
        db_tags = result.fetchall()
        if db_tags is None or len(db_tags) == 0:
            return None
        if len(db_tags) == 1 and db_tags[0][0] is None:
            return {}
        for tag, value in db_tags:
            if tag not in tags:
                tags[tag] = []
            tags[tag].append(value)
        return tags

    def get_files(self) -> Iterable[FileInfo]:
        result = self._connection.execute('SELECT path, modification_time AS "mtime [timestamp]" FROM files;')
        return (FileInfo(path, mtime) for path, mtime in result.fetchall())
