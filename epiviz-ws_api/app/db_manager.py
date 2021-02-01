from app.db import database, workspaces
from app import models
from uuid import uuid4

async def get_all_workspaces():
    query = workspaces.select()
    return await database.fetch_all(query)

async def get_user_workspaces(user_id: str):
    query = workspaces.select(workspaces.c.user_id == user_id)
    return await database.fetch_all(query)

async def get_workspace_tag(tag: str):
    query = workspaces.select(workspaces.c.tags.any(tag))
    return await database.fetch_all(query)

async def get_workspace(id: int):
    query = workspaces.select(workspaces.c.id == id)
    return await database.fetch_one(query)

async def get_workspace_uuid(uuid: str):
    query = workspaces.select(workspaces.c.workspace_uuid == uuid)
    return await database.fetch_one(query)

async def add_workspace(ws: models.WorkspaceCreate):
    tws = ws.dict()
    tws['workspace_uuid'] = str(uuid4()).split("-")[0]
    query = workspaces.insert().values(tws)
    try:
        id = await database.execute(query)
        return id, tws['workspace_uuid']
    except Exception as e:
        return add_workspace(**ws)

async def delete_workspace(id: int):
    query = workspaces.delete().where(workspaces.c.id == id)
    return await database.execute(query)

async def update_workspace(id: int, ws: models.WorkspaceUpdate):
    query = (
        workspaces
            .update()
            .where(workspaces.c.id == id)
            .values(**ws.dict())
    )
    return await database.execute(query=query)