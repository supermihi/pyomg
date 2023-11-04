from omg.brainz.model import ReleaseId, ArtistId, TrackId, WorkId
from omg.collection.entities import Release, TrackGroup, Work, Track, Artist, TrackGroupId


class CollectionStore:
    def __init__(self):
        self.releases_by_id: dict[ReleaseId, Release] = {}
        self.artists_by_id: dict[ArtistId, Artist] = {}
        self.tracks_by_id: dict[TrackId, Track] = {}
        self.track_groups_by_id: dict[TrackGroupId, TrackGroup] = {}
        self.works_by_id: dict[WorkId, Work] = {}

    def get_release(self, release_id: ReleaseId) -> Release | None:
        return self.releases_by_id.get(release_id)

    def add_release(self, release: Release):
        if release.id in self.releases_by_id:
            raise ValueError(f'release {release.id} ({release.title}) already in store')
        self.releases_by_id[release.id] = release

    def get_artist(self, artist_id: ArtistId) -> Artist | None:
        return self.artists_by_id.get(artist_id)

    def add_artist(self, artist: Artist):
        if artist.id in self.artists_by_id:
            raise ValueError(f'artist {artist.id} ({artist.name}) already in store')
        self.artists_by_id[artist.id] = artist

    def add_track(self, track: Track):
        if track.id in self.tracks_by_id:
            raise ValueError(f'track {track.id} ({track.title}) already in store')
        self.tracks_by_id[track.id] = track

    def get_track(self, track_id: TrackId) -> Track | None:
        return self.tracks_by_id.get(track_id)

    def get_work(self, work_id: WorkId) -> Work | None:
        return self.works_by_id.get(work_id)

    def add_track_group(self, track_group: TrackGroup):
        if track_group.id in self.track_groups_by_id:
            raise ValueError(f'track group {track_group} already in store')
        self.track_groups_by_id[track_group.id] = track_group

    def get_track_group(self, track_group_id: TrackGroupId) -> TrackGroup | None:
        return self.track_groups_by_id.get(track_group_id)
