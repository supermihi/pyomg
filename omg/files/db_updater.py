import logging
from pathlib import Path

from omg.files import FileInfo
from omg.files.sqlite import TagDatabase
from omg.files.tags import TagProvider
from omg.files.walker import AudioFileWalker


class DatabaseUpdater:

    def __init__(self, db: TagDatabase, tag_provider: TagProvider, walker: AudioFileWalker):
        self.db = db
        self.tag_provider = tag_provider
        self.walker = walker

    def update(self):
        db_files: dict[Path, FileInfo] = {file.path: file for file in self.db.get_files()}
        fs_files: dict[Path, FileInfo] = {file.path: file for file in self.walker.get_files()}

        db_paths = set(db_files.keys())
        fs_paths = set(fs_files.keys())

        for deleted_path in db_paths - fs_paths:
            self.db.remove_file(deleted_path)

        for new_path in fs_paths - db_paths:
            logging.info(f'scanning new file {new_path}')
            self.update_file_info(fs_files[new_path])

        for path in db_paths & fs_paths:
            if fs_files[path].mtime > db_files[path].mtime:
                logging.info(f'scanning modified file {path}')
                self.update_file_info(fs_files[path])

    def update_file_info(self, info: FileInfo):
        tags = self.tag_provider.get_tags(info.path)
        self.db.add_or_update(info, tags)
