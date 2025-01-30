from abc import ABC
from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound
from projectFiles.adapters.repository import AbstractRepository
from projectFiles.domainmodel.model import *

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.rollback()
    
    @property
    def session(self):
        return self.__session
    
    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()
    
    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)
    

class DatabaseRepository(AbstractRepository):

    def __init__(self, session_factory):
        super().__init__()
        self._session_cm = SessionContextManager(session_factory)
        
    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()
    
    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def remove_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.delete(track)
            scm.commit()

    def search_tracks(self, track_name: str) -> list[Track]:
        tracks = self._session_cm.session.query(Track).filter(Track.title.like(f"%{track_name}%")).all()
        return tracks

    @property
    def tracks(self) -> list[Track]:
        tracks = self._session_cm.session.query(Track).all()
        return tracks