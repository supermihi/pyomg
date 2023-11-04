from omg.collection.builder import CollectionBuilder
from omg.collection.entities import TrackGroup, TrackGroupId
from omg.collection.store import CollectionStore
from omg.test_utils.mbids import argerich_rach3_tchaik1, rach3, argerich_rach3_mvmt1, rach3_mvmt1


def test_add_release(musicbrainz_source):
    store = CollectionStore()
    builder = CollectionBuilder(store, musicbrainz_source)

    release = builder.get_or_add_release(argerich_rach3_tchaik1)

    assert len(release.contents) == 2

    for content in release.contents:
        assert isinstance(content, TrackGroupId)

    first_track_group = store.get_track_group(release.contents[0])
    assert first_track_group.work == rach3
    assert len(first_track_group.tracks) == 3

    first_track = store.get_track(first_track_group.tracks[0])
    assert first_track.recording_id == argerich_rach3_mvmt1
    assert first_track.works[0] == rach3_mvmt1
