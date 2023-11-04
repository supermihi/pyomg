from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Sequence

import requests

from omg.brainz.aliases import get_alias, Alias
from omg.brainz.model import RecordingId, WorkId, WorkRecording, ParentWork, ArtistId, ArtistData, WorkData, \
    RecordingData, RecordingArtistRelation, RecordingArtistRelationType, ReleaseId, ReleaseData, MediumData, TrackData
from omg.brainz.source import MusicbrainzDataSourceBase
from omg.util.dates import PartialDate


@dataclass
class MusicbrainzConfiguration:
    hostname: str = 'musicbrainz.org'
    use_https: bool = True
    rate_limit: bool = True

    @property
    def url(self):
        return f'http{"s" if self.use_https else ""}://{self.hostname}/ws/2'


class MusicbrainzApiDataSource(MusicbrainzDataSourceBase):

    def __init__(self, config: MusicbrainzConfiguration, preferred_locales: Sequence[str] = ('en',),
                 session: requests.Session = None):
        self.preferred_locales = preferred_locales
        self.config = config
        self.session = session or requests.Session()
        self.session.headers.update({'User-Agent': 'pyomg/0.0.1 ( https://github.com/supermihi/pyomg )',
                                     'Accept': 'application/json'})

    def _call(self, entity: str, mbid: str, include: str | Sequence[str] | None = None):
        full_url = f'{self.config.url}/{entity}/{mbid}'
        if isinstance(include, str):
            include = [include]
        query = {'inc': '+'.join(include)} if include else {}
        response = self.session.get(full_url, params=query)
        response.raise_for_status()
        return response.json()

    def get_recorded_work(self, recording: RecordingId) -> Sequence[WorkRecording]:
        result = self._call('recording', recording.mbid, 'work-rels')
        work_relations = result['relations']
        performances = [wr for wr in work_relations if is_performance(wr)]
        return [WorkRecording.from_work_relation(recording, p) for p in performances]

    def get_parent_works(self, work: WorkId) -> Sequence[ParentWork]:
        result = self._call('work', work.mbid, 'work-rels')
        work_relations = result['relations']
        part_ofs = [wr for wr in work_relations if is_part_of(wr)]
        return [ParentWork.from_work_relation(work, p) for p in part_ofs]

    def get_composers(self, work: WorkId) -> Sequence[ArtistId]:
        result = self._call('work', work.mbid, 'artist-rels')
        artist_rels = result['relations']
        composers = [ar for ar in artist_rels if is_composer(ar)]
        return [ArtistId(c['artist']['id']) for c in composers]

    def get_work_data(self, work: WorkId) -> WorkData:
        result = self._call('work', work.mbid, 'aliases')
        alias = get_alias(result['aliases'], self.preferred_locales)
        if alias is None:
            alias = Alias(result['title'], result.get('sort-name'))
        return WorkData(id=work, name=alias.name, disambiguation=result.get('disambiguation') or None)

    def get_artist_data(self, artist: ArtistId) -> ArtistData:
        result = self._call('artist', artist.mbid, 'aliases')
        alias = get_alias(result['aliases'], self.preferred_locales)
        if alias is None:
            alias = Alias(result['name'], result.get('sort-name'))
        return ArtistData(id=artist, name=alias.name, sort=alias.sort_name,
                          disambiguation=result.get('disambiguation') or None)

    def get_recording_data(self, recording: RecordingId) -> RecordingData:
        result = self._call('recording', recording.mbid)
        return RecordingData(id=recording, title=result['title'], disambiguation=result.get('disambiguation') or None,
                             length=timedelta(milliseconds=float(result['length'])))

    def get_recording_artists(self, recording: RecordingId) -> Sequence[RecordingArtistRelation]:
        result = self._call('recording', recording.mbid, 'artist-rels')
        relations = []
        for relation in result['relations']:
            if relation.get('direction') != 'backward':
                continue
            relation_type = RecordingArtistRelationType(relation['type'], tuple(relation.get('attributes', [])))
            artist = ArtistId(mbid=relation['artist']['id'])
            relations.append(RecordingArtistRelation(recording, artist, type=relation_type,
                                                     end_date=PartialDate.parse(relation.get('end'))))
        return relations

    def get_release_data(self, release: ReleaseId) -> ReleaseData:
        result = self._call('release', release.mbid, ('media', 'recordings', 'artists'))
        artists = parse_release_artists(result)
        media = tuple(parse_medium(m) for m in result['media'])
        return ReleaseData(id=release, title=result['title'],
                           date=PartialDate.parse(result['date']),
                           media=media,
                           credited_artists=artists)


def parse_medium(medium: dict) -> MediumData:
    return MediumData(position=medium['position'], format=medium['format'],
                      tracks=tuple(parse_track(t) for t in medium['tracks']))


def parse_track(track: dict) -> TrackData:
    return TrackData(position=track['position'], recording=RecordingId(track['recording']['id']),
                     track_id=track['id'])


def parse_release_artists(release: dict) -> Sequence[ArtistId]:
    result = []
    for artist_credit in release['artist-credit']:
        if isinstance(artist_credit, dict) and 'artist' in artist_credit:
            result.append(artist_credit['artist']['id'])
    return tuple(result)


def is_performance(work_relation: dict) -> bool:
    return work_relation.get('type') == 'performance' and work_relation.get('direction') == 'forward'


def is_part_of(work_relation: dict) -> bool:
    return work_relation.get('type') == 'parts' and work_relation.get('direction') == 'backward'


def is_composer(artist_relation: dict) -> bool:
    return artist_relation.get('type') == 'composer' and artist_relation.get('direction') == 'backward'
