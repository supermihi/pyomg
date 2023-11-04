from dataclasses import dataclass
from typing import Sequence

from omg.brainz.model import ArtistId, ArtistData, WorkId, TrackId, RecordingId, ReleaseId
from omg.util.dates import PartialDate


@dataclass
class Artist:
    id: ArtistId
    name: str
    sort_name: str
    disambiguation: str | None

    @staticmethod
    def from_musicbrainz(artist: ArtistData):
        return Artist(id=artist.id, name=artist.name, sort_name=artist.sort or artist.name,
                      disambiguation=artist.disambiguation)


@dataclass
class ParentWork:
    id: WorkId
    own_position: int


@dataclass
class Work:
    id: WorkId
    name: str
    disambiguation: str | None

    parent: ParentWork | None
    composers: Sequence[ArtistId]


@dataclass
class Track:
    id: TrackId
    recording_id: RecordingId
    title: str

    medium_number: int
    medium_format: str
    track_number: int

    works: Sequence[WorkId]
    artists: Sequence[ArtistId]


@dataclass(frozen=True)
class TrackGroupId:
    first_track: TrackId
    number_of_tracks: int


@dataclass
class TrackGroup:
    id: TrackGroupId
    work: WorkId
    tracks: Sequence[TrackId]

    def __str__(self):
        return f'Recording of {self.work} ({len(self.tracks)} tracks)'


@dataclass
class Release:
    id: ReleaseId
    title: str
    date: PartialDate
    artists: Sequence[ArtistId]

    contents: Sequence[TrackId | TrackGroupId]

    def __str__(self):
        return self.title if self.date is None else f'{self.title} ({self.date})'
