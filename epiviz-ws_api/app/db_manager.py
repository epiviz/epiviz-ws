from app.db import database, workspaces
from app import models

async def get_all_workspaces():
    query = workspaces.select()
    return await database.fetch_all(query)

async def get_user_workspaces(user_id: str):
    query = workspaces.select(workspaces.c.user_id == user_id)
    return await database.fetch_all(query)

async def get_workspace(id: int):
    query = workspaces.select(workspaces.c.id == id)
    return await database.fetch_one(query)

async def add_workspace(ws: models.WorkspaceCreate):
    query = workspaces.insert().values(**ws.dict())
    return await database.execute(query)

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