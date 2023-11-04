from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import timedelta

from omg.util.dates import PartialDate


@dataclass(frozen=True)
class RecordingId:
    mbid: str

@dataclass(frozen=True)
class TrackId:
    mbid: str

@dataclass(frozen=True)
class WorkId:
    mbid: str


@dataclass(frozen=True)
class ArtistId:
    mbid: str


@dataclass(frozen=True)
class ReleaseId:
    """Musicbraniz release id."""
    mbid: str


@dataclass(frozen=True)
class WorkRecording:
    """Work-recording relation."""
    recording: RecordingId
    work: WorkId

    @staticmethod
    def from_work_relation(recording: RecordingId, work_relation: dict) -> WorkRecording:
        """Create a Performance from a work-relation JSON object."""
        return WorkRecording(work=WorkId(work_relation['work']['id']), recording=recording)


@dataclass(frozen=True)
class ParentWork:
    parent_work: WorkId
    part: WorkId
    number: int

    @staticmethod
    def from_work_relation(work: WorkId, work_relation: dict) -> ParentWork:
        return ParentWork(
            parent_work=WorkId(work_relation['work']['id']),
            part=work,
            number=int(work_relation['ordering-key'])
        )


@dataclass(frozen=True)
class ArtistData:
    id: ArtistId
    name: str
    sort: str | None
    disambiguation: str | None


@dataclass(frozen=True)
class WorkData:
    id: WorkId
    name: str
    disambiguation: str | None


@dataclass(frozen=True)
class RecordingData:
    id: RecordingId
    title: str
    length: timedelta
    disambiguation: str | None


@dataclass(frozen=True)
class TrackData:
    position: int
    recording_id: RecordingId
    track_id: TrackId


@dataclass(frozen=True)
class MediumData:
    position: int
    format: str
    tracks: Sequence[TrackData]


@dataclass(frozen=True)
class ReleaseData:
    id: ReleaseId
    title: str
    credited_artists: Sequence[ArtistId]
    date: PartialDate
    media: Sequence[MediumData]


@dataclass(frozen=True)
class RecordingArtistRelationType:
    type: str
    attributes: Sequence[str] = tuple()


@dataclass(frozen=True)
class RecordingArtistRelation:
    recording: RecordingId
    artist: ArtistId
    end_date: PartialDate | None
    type: RecordingArtistRelationType
