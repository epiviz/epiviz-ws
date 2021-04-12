# https://fastapi.tiangolo.com/advanced/async-sql-databases/

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os

from app.workspaces import workspaces
from app.findings import findings

from app.db import Base

# create all tables
Base.Base.metadata.create_all(Base.engine)

# https://alembic.sqlalchemy.org/en/latest/cookbook.html#building-an-up-to-date-database-from-scratch
# TODO: only useful when building from scratch
# from alembic.config import Config
# from alembic import command
# alembic_cfg = Config("alembic.ini")
# command.stamp(alembic_cfg, "head")

openapi_prefix = os.getenv('OPENAPI_PREFIX', default='')
print("using api prefix" + openapi_prefix)

app = FastAPI(openapi_prefix=openapi_prefix, openapi_url='/api/v1/openapi.json', docs_url='/api/v1/docs')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workspaces, prefix='/api/v1', tags=['workspaces'])
app.include_router(findings, prefix='/api/v1/findings', tags=['findings'])