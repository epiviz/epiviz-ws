from app.api.models import WorkspaceIn, WorkspaceOut, WorkspaceUpdate
from app.api.db import workspaces, database

async def add_workspace(payload: WorkspaceIn):
    query = workspaces.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_workspaces():
    query = workspaces.select()
    return await database.fetch_all(query=query)

async def get_workspace(ws_id):
    query = workspaces.select(workspaces.c.ws_id == ws_id)
    return await database.fetch_one(query=query)

async def delete_workspace(ws_id):
    query = workspaces.delete().where(workspaces.c.ws_id == ws_id)
    return await database.execute(query=query)

async def update_workspace(ws_id, payload: WorkspaceIn):
    query = (
        workspaces
            .update()
            .where(workspaces.c.ws_id == ws_id)
            .values(**payload.dict())
    )
    return await database.execute(query=query)