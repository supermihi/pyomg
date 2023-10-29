from __future__ import annotations

from typing import Sequence

import musicbrainzngs

from omg.brainz.source import MusicbrainzDataSourceBase
from omg.brainz.model import Recording, Work, Performance, WorkPart, Artist


class MusicbrainzNgsDataSource(MusicbrainzDataSourceBase):

    def __init__(self):
        pass
        # musicbrainzngs.set_hostname('localhost', use_https=False)

    def get_performances(self, recording: Recording) -> Sequence[Performance]:
        result = musicbrainzngs.get_recording_by_id(recording.mbid, includes=['work-rels'])
        work_relations = result['recording']['work-relation-list']
        performances = [wr for wr in work_relations if is_performance(wr)]
        return [Performance.from_work_relation(recording, p) for p in performances]

    def get_enclosing(self, work: Work) -> Sequence[WorkPart]:
        result = musicbrainzngs.get_work_by_id(work.mbid, includes='work-rels')
        work_relations = result['work']['work-relation-list']
        part_ofs = [wr for wr in work_relations if is_part_of(wr)]
        return [WorkPart.from_work_relation(work, p) for p in part_ofs]

    def get_composers(self, work: Work) -> Sequence[Artist]:
        result = musicbrainzngs.get_work_by_id(work.mbid, includes='artist-rels')
        artist_rels = result['work']['artist-relation-list']
        composers = [ar for ar in artist_rels if is_composer(ar)]
        return [Artist(c['artist']['id']) for c in composers]


def is_performance(work_relation: dict) -> bool:
    return work_relation.get('type') == 'performance' and work_relation.get('direction') == 'forward'


def is_part_of(work_relation: dict) -> bool:
    return work_relation.get('type') == 'parts' and work_relation.get('direction') == 'backward'


def is_composer(artist_relation: dict) -> bool:
    return artist_relation.get('type') == 'composer' and artist_relation.get('direction') == 'backward'
