from __future__ import annotations
from abc import abstractmethod, ABC
from collections.abc import Sequence

from omg.brainz.model import Recording, Work, Performance, WorkPart


class MusicbrainzDataSourceBase(ABC):

    @abstractmethod
    def get_performances(self, recording: Recording) -> Sequence[Performance]:
        """Get all 'Performance' objects that point to this recording."""
        pass

    @abstractmethod
    def get_enclosing(self, work: Work) -> Sequence[WorkPart]:
        pass


