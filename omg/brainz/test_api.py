from datetime import timedelta

import pytest

from omg.brainz.model import WorkId, WorkRecording, ParentWork, ArtistId, ArtistData, WorkData, \
    RecordingData, RecordingArtistRelation, RecordingArtistRelationType
from omg.test_utils.mbids import rach3_mvmt1, rach3_mvmt2, argerich_rach3_mvmt1, rach3, rach, argerich_rach3_tchaik1
from omg.util.dates import PartialDate


@pytest.mark.locales('de', 'en')
def test_recording_performances(musicbrainz_source):
    works = musicbrainz_source.get_recorded_work(argerich_rach3_mvmt1)

    expected = WorkRecording(argerich_rach3_mvmt1, rach3_mvmt1)

    assert len(works) == 1
    assert works[0] == expected


@pytest.mark.parametrize(('work', 'index'), [(rach3_mvmt1, 1), (rach3_mvmt2, 2)])
def test_work_work(musicbrainz_source, work: WorkId, index: int):
    works = musicbrainz_source.get_parent_works(work)

    expected = ParentWork(parent_work=rach3, part=work, number=index)

    assert len(works) == 1
    assert works[0] == expected


@pytest.mark.parametrize('work', (rach3_mvmt2, rach3))
def test_get_composers(musicbrainz_source, work: WorkId):
    artists = musicbrainz_source.get_composers(work)

    assert len(artists) == 1
    assert artists[0] == rach


@pytest.mark.locales('de')
def test_get_artist_data(musicbrainz_source):
    result = musicbrainz_source.get_artist_data(rach)

    expected = ArtistData(id=rach, name='Sergei Rachmaninow',
                          sort='Rachmaninow, Sergei', disambiguation='Russian composer')

    assert result == expected


def test_get_work_data(musicbrainz_source):
    result = musicbrainz_source.get_work_data(rach3_mvmt2)
    expected = WorkData(id=rach3_mvmt2,
                        name='Konzert für Klavier und Orchester Nr. 3 D-Moll, Op. 30: II. Intermezzo. Adagio',
                        disambiguation=None)

    assert result == expected


def test_get_recording_data(musicbrainz_source):
    result = musicbrainz_source.get_recording_data(argerich_rach3_mvmt1)
    expected = RecordingData(id=argerich_rach3_mvmt1,
                             title='Piano Concerto no. 3 in D minor, op. 30: I. Allegro ma non tanto',
                             length=timedelta(seconds=946),
                             disambiguation=None)

    assert result == expected


def test_get_recording_artists(musicbrainz_source):
    result = musicbrainz_source.get_recording_artists(argerich_rach3_mvmt1)

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


def test_get_release(musicbrainz_source):
    release = musicbrainz_source.get_release_data(argerich_rach3_tchaik1)

    assert release.title == 'Rachmaninoff 3 / Tchaikovsky 1'
    assert release.date == PartialDate(1995)
    assert release.id == argerich_rach3_tchaik1

    assert len(release.media) == 1
    medium = release.media[0]

    assert len(medium.tracks) == 6

    assert medium.tracks[0].recording_id == argerich_rach3_mvmt1

    assert len(release.credited_artists) == 5
