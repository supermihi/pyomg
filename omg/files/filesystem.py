from pathlib import Path

import taglib

from omg.files.tags import Tags, TagProvider


class FilesystemTagProvider(TagProvider):

    def __init__(self, root: Path):
        self.root = root

    def _ensure_abs(self, path: Path):
        if path.is_absolute():
            return path
        return self.root / path

    def get_tags(self, path: Path) -> Tags:
        with taglib.File(self._ensure_abs(path)) as taglib_file:
            return taglib_file.tags
