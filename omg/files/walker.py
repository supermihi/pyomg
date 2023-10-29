from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path, PurePath
from typing import Iterable

from omg.files import FileInfo


class AudioFileWalker(ABC):
    @abstractmethod
    def get_files(self) -> Iterable[FileInfo]:
        raise NotImplementedError()


class FilesystemAudioFileWalker(AudioFileWalker):

    @staticmethod
    def is_audio_file(path: PurePath):
        return path.suffix.lower() in ('.mp3', '.ogg', '.flac', '.m4a', '.mp4', '.wav', '.wma', '.mpc')

    def __init__(self, root: Path):
        if not root.exists():
            raise ValueError(f'root path {root} must exist in the filesystem')
        if not root.is_dir():
            raise ValueError(f'root path {root} must be a directory')
        self.root = root.resolve()

    def get_files(self) -> Iterable[FileInfo]:
        for path in self.root.glob('**/*'):
            if self.is_audio_file(path):
                yield FileInfo(path, datetime.fromtimestamp(path.stat().st_mtime))
