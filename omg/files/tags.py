from abc import ABC, abstractmethod
from pathlib import Path
from typing import Mapping, Sequence

Tags = Mapping[str, Sequence[str]]


class TagProvider(ABC):

    @abstractmethod
    def get_tags(self, path: Path) -> Tags:
        raise NotImplementedError()
