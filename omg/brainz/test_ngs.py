from datetime import timedelta

import pytest

from omg.brainz.model import RecordingId, WorkId, WorkRecording, ParentWork, ArtistId, ArtistData, WorkData, \
    RecordingData, RecordingArtistRelation, RecordingArtistRelationType
from omg.brainz.ngs import MusicbrainzNgsDataSource
from omg.util.dates import PartialDate

rach3_mvmt1 = WorkId('e55e8d47-c07a-31f5-90e4-404b8e975255')
rach3_mvmt2 = WorkId('3daf2401-b558-3212-b70e-cb738749e02d')
argerich_rach3_mvmt1 = RecordingId('c2f6529a-bb42-41e6-b98a-a0431c19f24a')
rach3 = WorkId('21b5596b-5b70-320c-bf3f-c7285f770783')
rach = ArtistId('44b16e44-da77-4580-b851-0d765904573e')


def test_recording_performances():
    b = MusicbrainzNgsDataSource()

    works = b.get_recorded_work(argerich_rach3_mvmt1)

    expected = WorkRecording(argerich_rach3_mvmt1, rach3_mvmt1)

    assert len(works) == 1
    assert works[0] == expected


@pytest.mark.parametrize(('work', 'index'), [(rach3_mvmt1, 1), (rach3_mvmt2, 2)])
def test_work_work(work: WorkId, index: int):
    b = MusicbrainzNgsDataSource()
    works = b.get_parent_works(work)

    expected = ParentWork(parent_work=rach3, part=work, number=index)

    assert len(works) == 1
    assert works[0] == expected


@pytest.mark.parametrize('work', (rach3_mvmt2, rach3))
def test_get_composers(work: WorkId):
    s = MusicbrainzNgsDataSource()
    artists = s.get_composers(work)

    assert len(artists) == 1
    assert artists[0] == rach


def test_get_artist_data():
    s = MusicbrainzNgsDataSource(preferred_locales=('de',))
    result = s.get_artist_data(rach)

    expected = ArtistData(id=rach, name='Sergei Rachmaninow',
                          sort='Rachmaninow, Sergei', disambiguation='Russian composer')

    assert result == expected


def test_get_work_data():
    s = MusicbrainzNgsDataSource(preferred_locales=('de',))
    result = s.get_work_data(rach3_mvmt2)
    expected = WorkData(id=rach3_mvmt2,
                        name='Konzert für Klavier und Orchester Nr. 3 D-Moll, Op. 30: II. Intermezzo. Adagio',
                        disambiguation=None)

    assert result == expected


def test_get_recording_data():
    s = MusicbrainzNgsDataSource(preferred_locales=('en', 'de'))
    result = s.get_recording_data(argerich_rach3_mvmt1)
    expected = RecordingData(id=argerich_rach3_mvmt1,
                             title='Piano Concerto no. 3 in D minor, op. 30: I. Allegro ma non tanto',
                             length=timedelta(seconds=946),
                             disambiguation=None)

    assert result == expected

def test_get_recording_artists():
    s = MusicbrainzNgsDataSource(preferred_locales=('de',))
    result = s.get_recording_artists(argerich_rach3_mvmt1)

    conductor = RecordingArtistRelation(
        artist=ArtistId('28accaf9-3a4b-4052-b9d3-8033d3137d2d'),
        recording=argerich_rach3_mvmt1,
        type=RecordingArtistRelationType('conductor'),
        end_date=PartialDate(1982, 12)
    )
    pianist = RecordingArtistRelation(
        artist=ArtistId('3bb8b89e-5700-4d7a-aa0b-d48f8706831d'),
        recording=argerich_rach3_mvmt1,
        type=RecordingArtistRelationType('instrument', ('piano',)),
        end_date=PartialDate(1982, 12)
    )
    orchestra = RecordingArtistRelation(
        artist=ArtistId('5010b425-bf4e-41b1-93a7-f8729794558b'),
        recording=argerich_rach3_mvmt1,
        type=RecordingArtistRelationType('performing orchestra'),
        end_date=PartialDate(1982, 12)
    )

    assert set(result) == {pianist, conductor, orchestra}