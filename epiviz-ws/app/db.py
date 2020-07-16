from sqlalchemy import (Column, Integer, MetaData, String, Table, create_engine, ARRAY)
from databases import Database

DATABASE_URL = 'postgresql://localhost/epiviz-ws_db'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

workspaces = Table(
    'workspaces',
    metadata,
    Column('user_id', String, primary_key=True),
    Column('ws_id', Integer, primary_key=True),
    Column('title', String, nullable=True),
    Column('description', String, nullable=True),
    Column('genomes', ARRAY(String)),
    Column('tags', ARRAY(String), nullable=True),
    Column('ws_def', String)
)

database = Database(DATABASE_URL)
