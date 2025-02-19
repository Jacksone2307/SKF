from flask import session
from projectFiles.domainmodel.model import *
import projectFiles.adapters.repository as repo


repo_instance : repo.AbstractRepository = repo.repo_instance



def create_playlist(name):
    user = session["user"]["userinfo"]["email"]
    playlist = Playlist(user, name)
    repo_instance.add_playlist(user, playlist)

def get_playlists(user) -> list[Playlist]:
    return repo_instance.get_user_playlists(user)

def search_playlists(name) -> list[Playlist]:
    user = session["user"]["userinfo"]["email"]
    if name is None:
        return get_playlists(user)
    return repo_instance.search_playlists(user, name)

def get_track(track_id) -> list[Track]:
    return repo_instance.get_track(track_id)

def add_to_playlist(playlist: Playlist, track: Track):
    user = session["user"]["userinfo"]["email"]
    playlist.add_track(track)
    repo_instance.update_playlist(playlist)

def search_tracks(playlist_name, track_name):
    """LAST HERE, SEARCHING WAS JUST SEARCHING THROUGH ALL TRACKS, SHOWING TRACKS NOT IN PLAYLIST."""
    return repo_instance.search_tracks_in_playlist(playlist_name, track_name)