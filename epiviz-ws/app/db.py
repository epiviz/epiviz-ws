import sqlalchemy
import databases

DATABASE_URL = 'postgresql://localhost/epiviz-ws_db'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

workspaces = sqlalchemy.Table(
    'workspaces',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column('workspace_id', sqlalchemy.String, index=True),
    sqlalchemy.Column('user_id', sqlalchemy.String),
    sqlalchemy.Column('title', sqlalchemy.String, nullable=True),
    sqlalchemy.Column('description', sqlalchemy.String, nullable=True),
    sqlalchemy.Column('genomes', sqlalchemy.ARRAY(sqlalchemy.String), nullable=True),
    sqlalchemy.Column('tags', sqlalchemy.ARRAY(sqlalchemy.String), nullable=True),
    sqlalchemy.Column('workspace', sqlalchemy.String)
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

# https://alembic.sqlalchemy.org/en/latest/cookbook.html#building-an-up-to-date-database-from-scratch
from alembic.config import Config
from alembic import command
alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")
