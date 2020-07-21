# https://fastapi.tiangolo.com/advanced/async-sql-databases/

from fastapi import FastAPI, Depends
from app.db import database
from app.workspaces import workspaces

app = FastAPI(openapi_url='/api/v1/openapi.json', docs_url='/api/v1/docs')
        
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(workspaces, prefix='/api/v1', tags=['workspaces'])


