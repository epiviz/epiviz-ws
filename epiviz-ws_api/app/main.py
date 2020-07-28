# https://fastapi.tiangolo.com/advanced/async-sql-databases/

from fastapi import FastAPI, Depends
from app.db import database
from app.workspaces import workspaces
from fastapi.middleware.cors import CORSMiddleware
import os

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

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(workspaces, prefix='/api/v1', tags=['workspaces'])


