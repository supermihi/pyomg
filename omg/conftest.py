from pathlib import Path

import pytest
import requests_cache
from _pytest.fixtures import SubRequest

from omg.brainz.api import MusicbrainzConfiguration, MusicbrainzApiDataSource


@pytest.fixture(scope='session')
def testdata():
    return Path(__file__).resolve().parent.parent / 'testdata'


@pytest.fixture(scope='session')
def caching_session(testdata):
    test_cache = testdata / 'requests_cache.sqlite'
    session = requests_cache.CachedSession(str(test_cache), backend='sqlite')
    return session


@pytest.fixture
def musicbrainz_source(request: SubRequest, caching_session):
    config = MusicbrainzConfiguration()
    locale_marker = request.node.get_closest_marker('locales')
    if locale_marker is None:
        locales = ['en', 'de']
    else:
        locales = locale_marker.args
    source = MusicbrainzApiDataSource(config, preferred_locales=locales, session=caching_session)
    return source
