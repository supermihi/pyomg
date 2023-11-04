from omg.brainz.model import RecordingId, ReleaseId, RecordingData, ReleaseData
from omg.brainz.source import MusicbrainzDataSourceBase


class MusicCollection:

    def __init__(self, brainz_source: MusicbrainzDataSourceBase):
        self.brainz_source = brainz_source

    def add_recording(self, recording: RecordingId, release: ReleaseId) -> RecordingData:
        pass

    def add_release(self, release: ReleaseId) -> ReleaseData:
        pass

