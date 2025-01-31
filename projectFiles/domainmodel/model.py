from datetime import date
import string

class Track:
    """Class representing a musical track."""
    def __init__(self, title, url, key=None, id=None):
        self.title = string.capwords(title)
        self.url = url
        if key is not None:
            self.key = key
        self.date = date.today()
    
    @property
    def title(self) -> str:
        return self.title
    
    @property 
    def url(self) -> str:
        return self.url
    @url.setter
    def url(self, url):
        self.url = url

    @property
    def key(self) -> str:
        return self.key
    @key.setter
    def key(self, key):
        self.key = key

    def __eq__(self, other) -> bool:
        if not isinstance(other, Track):
            return False
        return self.title.lower().strip() == other.title.lower().strip() and self.url.lower() == other.url.lower()
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Track):
            return False
        return self.date < other.date
    
    def __repr__(self) -> str:
        return f"Track: {self.title}, {self.url}, {self.key}, {self.date}"
    
    def __hash__(self) -> int:
        return hash(self.title) + hash(self.url)
    
class Playlist:
    """Class representing a playlist, can hold multiple tracks."""
    def __init__(self, user, title="Untitled", tracks=None):
        self.user = user
        self.title = title
        if tracks is None:
            self.tracks = {}
        else:
            self.tracks = tracks
    
    def add_track(self, track):
        if hash(track) not in self.tracks:
            self.tracks[hash(track)] = track
        else:
            print("Track already in playlist")
    
    def remove_track(self, track):
        if hash(track) in self.tracks:
            self.tracks.pop(hash(track))
        else:
            print("Track not in playlist")
    
    def __repr__(self) -> str:
        return f"Playlist: {self.title}, {self.user}: " + str([self.tracks[key].title for key in self.tracks]) 

    