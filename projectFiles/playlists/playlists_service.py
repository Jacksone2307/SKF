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
