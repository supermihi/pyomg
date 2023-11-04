import itertools
import logging

from omg.brainz.model import ReleaseId, MediumData, TrackData, TrackId, ArtistId, WorkId
from omg.brainz.source import MusicbrainzDataSourceBase
from omg.collection.entities import Release, Track, TrackGroupId, ParentWork, TrackGroup, Artist, Work
from omg.collection.store import CollectionStore

logger = logging.getLogger(__name__)


class CollectionBuilder:

    def __init__(self, store: CollectionStore, brainz_source: MusicbrainzDataSourceBase):
        self.brainz_source = brainz_source
        self.store = store

    def get_or_add_release(self, release_id: ReleaseId) -> Release:
        existing = self.store.get_release(release_id)
        if existing is not None:
            return existing

        release_data = self.brainz_source.get_release_data(release_id)
        artists = tuple(release_data.credited_artists)
        for artist in artists:
            self.get_or_add_artist(artist)

        tracks = [self.create_track(medium, track) for medium in release_data.media for track in medium.tracks]

        contents = self.group_tracks(tracks)

        release = Release(release_id, title=release_data.title, date=release_data.date,
                          artists=artists, contents=contents)
        self.store.add_release(release)
        return release

    def create_track(self, medium_data: MediumData, track_data: TrackData) -> Track:
        recording_data = self.brainz_source.get_recording_data(track_data.recording_id)

        works = self.brainz_source.get_recorded_work(recording_data.id)
        for work in works:
            self.get_or_add_work(work.work)
        artists = self.brainz_source.get_recording_artists(recording_data.id)
        track = Track(id=track_data.track_id, recording_id=track_data.recording_id,
                      title=recording_data.title,
                      medium_number=medium_data.position,
                      medium_format=medium_data.format,
                      track_number=track_data.position,
                      works=[w.work for w in works],
                      artists=[relation.artist for relation in artists])
        self.store.add_track(track)
        return track

    def group_tracks(self, tracks: list[Track]) -> tuple[TrackId | TrackGroupId, ...]:
        def group_key(t: Track):
            if len(t.works) == 0:
                return t.id
            work = self.get_or_add_work(t.works[0])
            if work.parent is None:
                return t.id
            return work.parent.id

        result: list[TrackId | TrackGroupId] = []

        tracks_by_parent_work = itertools.groupby(tracks, key=group_key)
        for key, group in tracks_by_parent_work:
            tracks = list(group)
            if isinstance(key, WorkId):
                track_group_id = TrackGroupId(tracks[0].id, len(tracks))
                track_group = TrackGroup(track_group_id, key, [t.id for t in tracks])
                self.store.add_track_group(track_group)
                result.append(track_group.id)
            else:
                assert len(tracks) == 1
                result.append(tracks[0].id)
        return tuple(result)

    def get_or_add_artist(self, artist_id: ArtistId) -> Artist:
        existing = self.store.get_artist(artist_id)
        if existing is not None:
            return existing

        artist_data = self.brainz_source.get_artist_data(artist_id)
        artist = Artist(id=artist_id, name=artist_data.name, sort_name=artist_data.sort or artist_data.name,
                        disambiguation=artist_data.disambiguation)
        self.store.add_artist(artist)
        return artist

    def get_or_add_work(self, work_id: WorkId) -> Work:
        existing = self.store.get_work(work_id)
        if existing is not None:
            return existing

        work_data = self.brainz_source.get_work_data(work_id)
        composers = self.brainz_source.get_composers(work_id)
        for composer in composers:
            self.get_or_add_artist(composer)

        parents = self.brainz_source.get_parent_works(work_id)
        if len(parents) > 1:
            logger.warning(f'work {work_data} has multiple parents; ignoring all but first')
        parent = ParentWork(parents[0].parent_work, parents[0].number) if len(parents) > 0 else None
        work = Work(id=work_id, name=work_data.name, disambiguation=work_data.disambiguation,
                    composers=tuple(composers), parent=parent)
        return work
