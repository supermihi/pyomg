from __future__ import annotations
from abc import abstractmethod, ABC
from collections.abc import Sequence

from omg.brainz.model import RecordingId, WorkId, WorkRecording, ParentWork, ArtistId, ArtistData, ReleaseId, \
    ReleaseData


class MusicbrainzDataSourceBase(ABC):

    @abstractmethod
    def get_recorded_work(self, recording: RecordingId) -> Sequence[WorkRecording]:
        """Get all 'WorkRecording' objects that point to this recording."""
        pass

    @abstractmethod
    def get_parent_works(self, work: WorkId) -> Sequence[ParentWork]:
        pass

    @abstractmethod
    def get_composers(self, work: WorkId) -> Sequence[ArtistId]:
        pass

    @abstractmethod
    def get_artist_data(self, artist: ArtistId) -> ArtistData:
        pass

    @abstractmethod
    def get_release_data(self, release: ReleaseId) -> ReleaseData:
        pass
