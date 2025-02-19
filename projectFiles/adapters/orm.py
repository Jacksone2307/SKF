from projectFiles.domainmodel.model import *
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import registry, relationship

mapper_registry = registry()

tracks_table = Table(
    "tracks", mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String),
    Column("url", String),
    Column("key", String, nullable=True),
    Column("date", Date)
)

playlists_table = Table(
    "playlists", mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user", String),
    Column("title", String)
)

playlist_tracks_table = Table(
    "playlist_tracks", mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("playlist_id", Integer, ForeignKey('playlists.id')),
    Column("track_id", Integer, ForeignKey('tracks.id'))
)


def map():
    mapper_registry.map_imperatively(Track, tracks_table, properties={
        'title': tracks_table.c.title,
        'url': tracks_table.c.url,
        'key': tracks_table.c.key,
        'date': tracks_table.c.date,
        'id': tracks_table.c.id
    })

    mapper_registry.map_imperatively(Playlist, playlists_table, properties={
        'title': playlists_table.c.title,
        'user': playlists_table.c.user,
        'id': playlists_table.c.id,
        'tracks': relationship(Track, secondary=playlist_tracks_table)
    })

