from datetime import date

class Track:
    """Class representing a musical track."""
    def __init__(self, title, url, key=None):
        self.title = title
        self.url = url
        if self.key is not None:
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
        return self.title == other.title and self.url == other.url and self.key == other.key
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Track):
            return False
        return hash(self.date) < hash(other.date)

    