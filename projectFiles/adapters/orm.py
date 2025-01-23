from projectFiles.domainmodel.model import *
from sqlalchemy import Table, Column, Integer, String, Date
from sqlalchemy.orm import registry

mapper_registry = registry()

tracks_table = Table(
    "tracks", mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String),
    Column("url", String),
    Column("key", String, nullable=True)
)


def map():
    mapper_registry.map_imperatively(Track, tracks_table, properties={
        'title': tracks_table.c.title,
        'url': tracks_table.c.url,
        'key': tracks_table.c.key,
    })
