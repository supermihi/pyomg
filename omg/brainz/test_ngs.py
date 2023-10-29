import pytest

from omg.brainz.model import Recording, Work, Performance, WorkPart, Artist
from omg.brainz.ngs import MusicbrainzNgsDataSource

rach3_mvmt1 = Work('e55e8d47-c07a-31f5-90e4-404b8e975255')
rach3_mvmt2 = Work('3daf2401-b558-3212-b70e-cb738749e02d')
argerich_rach3_mvmt1 = Recording('c2f6529a-bb42-41e6-b98a-a0431c19f24a')
rach3 = Work('21b5596b-5b70-320c-bf3f-c7285f770783')
rach = Artist('44b16e44-da77-4580-b851-0d765904573e')


def test_recording_performances():
    b = MusicbrainzNgsDataSource()

    works = b.get_performances(argerich_rach3_mvmt1)

    expected = Performance(argerich_rach3_mvmt1, rach3_mvmt1)

    assert len(works) == 1
    assert works[0] == expected


@pytest.mark.parametrize(('work', 'index'), [(rach3_mvmt1, 1), (rach3_mvmt2, 2)])
def test_work_work(work: Work, index: int):
    b = MusicbrainzNgsDataSource()
    works = b.get_enclosing(work)

    expected = WorkPart(enclosing_work=rach3, part=work, number=index)

    assert len(works) == 1
    assert works[0] == expected


@pytest.mark.parametrize('work', (rach3_mvmt2, rach3))
def test_get_composers(work: Work):
    s = MusicbrainzNgsDataSource()
    artists = s.get_composers(work)

    assert len(artists) == 1
    assert artists[0] == rach
