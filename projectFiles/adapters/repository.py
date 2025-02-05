import abc

from projectFiles.domainmodel.model import *


repo_instance = None

class AbstractRepository(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def add_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_track(self, track: Track):
        raise NotImplementedError
    
    @property
    def tracks(self) -> list[Track]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def search_tracks(self, track_name: str) -> list[Track]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_playlist(self, playlist: Playlist):
        raise NotImplementedError
    
    @abc.abstractmethod
    def remove_playlist(self, playlist: Playlist):
        raise NotImplementedError
    
    @property
    def playlists(self) -> list[Playlist]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def search_playlists(self,  playlist_name: str) -> list[Track]:
        raise NotImplementedError