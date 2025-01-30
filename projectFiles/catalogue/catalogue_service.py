from projectFiles.domainmodel.model import *
import projectFiles.adapters.repository as repo

repo_instance : repo.AbstractRepository = repo.repo_instance

def get_tracks():
    return repo_instance.tracks

def search_tracks(track_name):
    return repo_instance.search_tracks(track_name)
    