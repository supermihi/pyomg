from __future__ import annotations

from datetime import timedelta
from typing import Sequence

import musicbrainzngs

from omg.brainz.aliases import get_alias, Alias
from omg.brainz.model import RecordingId, WorkId, WorkRecording, ParentWork, ArtistId, ArtistData, WorkData, \
    RecordingData, RecordingArtistRelation, RecordingArtistRelationType
from omg.util.dates import PartialDate
from omg.brainz.source import MusicbrainzDataSourceBase


class MusicbrainzNgsDataSource(MusicbrainzDataSourceBase):

    def __init__(self, preferred_locales: Sequence[str] = ('de', 'en')):
        self.preferred_locales = preferred_locales
        # musicbrainzngs.set_hostname('localhost', use_https=False)

    def get_recorded_work(self, recording: RecordingId) -> Sequence[WorkRecording]:
        result = musicbrainzngs.get_recording_by_id(recording.mbid, includes=['work-rels'])
        work_relations = result['recording']['work-relation-list']
        performances = [wr for wr in work_relations if is_performance(wr)]
        return [WorkRecording.from_work_relation(recording, p) for p in performances]

    def get_parent_works(self, work: WorkId) -> Sequence[ParentWork]:
        result = musicbrainzngs.get_work_by_id(work.mbid, includes='work-rels')
        work_relations = result['work']['work-relation-list']
        part_ofs = [wr for wr in work_relations if is_part_of(wr)]
        return [ParentWork.from_work_relation(work, p) for p in part_ofs]

    def get_composers(self, work: WorkId) -> Sequence[ArtistId]:
        result = musicbrainzngs.get_work_by_id(work.mbid, includes='artist-rels')
        artist_rels = result['work']['artist-relation-list']
        composers = [ar for ar in artist_rels if is_composer(ar)]
        return [ArtistId(c['artist']['id']) for c in composers]

    def get_work_data(self, work: WorkId) -> WorkData:
        result = musicbrainzngs.get_work_by_id(work.mbid, includes=['aliases'])['work']
        alias = get_alias(result['alias-list'], self.preferred_locales)
        if alias is None:
            alias = Alias(result['title'], result.get('sort-name'))
        return WorkData(id=work, name=alias.name, disambiguation=result.get('disambiguation'))

    def get_artist_data(self, artist: ArtistId) -> ArtistData:
        result = musicbrainzngs.get_artist_by_id(artist.mbid, includes=['aliases'])['artist']
        alias = get_alias(result['alias-list'], self.preferred_locales)
        if alias is None:
            alias = Alias(result['name'], result.get('sort-name'))
        return ArtistData(id=artist, name=alias.name, sort=alias.sort_name, disambiguation=result.get('disambiguation'))

    def get_recording_data(self, recording: RecordingId) -> RecordingData:
        result = musicbrainzngs.get_recording_by_id(recording.mbid)['recording']
        return RecordingData(id=recording, title=result['title'], disambiguation=result.get('disambiguation'),
                             length=timedelta(milliseconds=float(result['length'])))

    def get_recording_artists(self, recording: RecordingId) -> Sequence[RecordingArtistRelation]:
        result = musicbrainzngs.get_recording_by_id(recording.mbid, includes=['artist-rels'])['recording']
        relations = []
        for relation in result['artist-relation-list']:
            if relation.get('direction') != 'backward':
                continue
            relation_type = RecordingArtistRelationType(relation['type'], tuple(relation.get('attribute-list', [])))
            artist = ArtistId(mbid=relation['target'])
            relations.append(RecordingArtistRelation(recording, artist, type=relation_type,
                                                     end_date=PartialDate.parse(relation.get('end'))))
        return relations


def is_performance(work_relation: dict) -> bool:
    return work_relation.get('type') == 'performance' and work_relation.get('direction') == 'forward'


def is_part_of(work_relation: dict) -> bool:
    return work_relation.get('type') == 'parts' and work_relation.get('direction') == 'backward'


def is_composer(artist_relation: dict) -> bool:
    return artist_relation.get('type') == 'composer' and artist_relation.get('direction') == 'backward'
