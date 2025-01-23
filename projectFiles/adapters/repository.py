import abc

from projectFiles.domainmodel.model import *


repo_instance = None

class AbstractRepository(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def add_track(self, track: Track):
        raise NotImplementedError

    def remove_track(self, track: Track):
        raise NotImplementedError
    
    @property
    def tracks(self) -> list[Track]:
        raise NotImplementedError