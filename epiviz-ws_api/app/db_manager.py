from app.db import database, workspaces
from app import models

async def get_all_workspaces():
    query = workspaces.select()
    return await database.fetch_all(query)

async def get_workspace(workspace_id: int):
    query = workspaces.select(workspaces.c.workspace_id == workspace_id)
    return await database.fetch_one(query)

async def add_workspace(ws: models.WorkspaceCreate):
    query = workspaces.insert().values(**ws.dict())
    return await database.execute(query)

async def delete_workspace(workspace_id: str):
    query = workspaces.delete().where(workspaces.c.workspace_id == workspace_id)
    return await database.execute(query)

async def update_workspace(workspace_id, ws: models.WorkspaceUpdate):
    query = (
        workspaces
            .update()
            .where(workspaces.c.workspace_id == workspace_id)
            .values(**ws.dict())
    )
    return await database.execute(query=query)