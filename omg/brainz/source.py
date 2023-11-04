from __future__ import annotations
from abc import abstractmethod, ABC
from collections.abc import Sequence

from omg.brainz.model import RecordingId, WorkId, WorkRecording, ParentWork, ArtistId, ArtistData, ReleaseId, \
    ReleaseData, RecordingData, RecordingArtistRelation, WorkData


class MusicbrainzDataSourceBase(ABC):

    @abstractmethod
    def get_recorded_work(self, recording_id: RecordingId) -> Sequence[WorkRecording]:
        """Get all 'WorkRecording' objects that point to this recording."""
        pass

    @abstractmethod
    def get_parent_works(self, work: WorkId) -> Sequence[ParentWork]:
        pass

    @abstractmethod
    def get_composers(self, work: WorkId) -> Sequence[ArtistId]:
        pass

    @abstractmethod
    def get_work_data(self, work_id: WorkId) -> WorkData:
        pass

    @abstractmethod
    def get_artist_data(self, artist_id: ArtistId) -> ArtistData:
        pass

    @abstractmethod
    def get_recording_data(self, recording_id: RecordingId) -> RecordingData:
        pass

    @abstractmethod
    def get_recording_artists(self, recording_id: RecordingId) -> Sequence[RecordingArtistRelation]:
        pass

    @abstractmethod
    def get_release_data(self, release_id: ReleaseId) -> ReleaseData:
        pass
