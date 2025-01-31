import requests
from googlesearch import search
import re
import concurrent.futures
from projectFiles.domainmodel.model import *
import projectFiles.adapters.repository as repo


repo_instance : repo.AbstractRepository = repo.repo_instance

class SongNotFoundError(Exception):
    """Raised when the key can't be found in key_search()"""
    def __init__(self, qry):
        self.qry = qry

    def __str__(self):
         return f"'{self.qry}' not found."


def remove_html_tags(text):
    """Remove html tags from a string"""

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
    
def get_auth_header(token):
     return {"Authorization": "Bearer " + token}


def search_and_open_video(qry):
    """Search for the song on youtube, and return the url of the first video, ready for autoplay."""
    yt_qry = qry + " youtube"
    for i in search(yt_qry, num=1, stop=1):
            id = i.split("=")[1]
            url = f"https://www.youtube.com/embed/{id}?autoplay=1&mute=1"
            return url

def key_search(qry):
    """Search for the key of the song on songbmp, and return the first one."""
    google_qry = qry + " songbpm key"
    for i in search(google_qry, num=1, stop=1):
            r = requests.get(i)
            text = remove_html_tags(str(r.content))
            key = re.search('with a ([A-G]) key and a (.*) mode', text)
            try:
                if key is None:
                     raise SongNotFoundError(qry)
                print("Found KEY")
                return f"{key.group(1)} {key.group(2)}"
            except Exception as e:
                 return ""
    
    
                 

def induce_search(qry, get_key):
    """Search for the song and video independently."""
    key = None
    if get_key:
        ###Find the key, with a timeout of 11 seconds.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(key_search, qry)
            try:
                key = future.result(timeout=16)
            except concurrent.futures.TimeoutError:
                 key = ""
                 
    url = search_and_open_video(qry)
    return key, url


def save_track_to_db(track_to_save: Track):
    similarTracks = repo_instance.search_tracks(track_to_save.title)
    for track in similarTracks:
         if track == track_to_save:
              return 1
    repo_instance.add_track(track_to_save)