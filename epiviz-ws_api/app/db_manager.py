from app.db import database, workspaces, findings
from app import models
from uuid import uuid4

# Workspaces
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

async def get_workspace_findings(id:int):
    query = findings.select(findings.c.workspace_id == id)
    res =  await database.fetch_all(query)
    print(res)
    return res

# Findings
async def get_all_findings():
    query = findings.select()
    return await database.fetch_all(query)

async def get_user_findings(user_id: str):
    query = findings.select(findings.c.user_id == user_id)
    return await database.fetch_all(query)

async def get_finding(id: int):
    query = findings.select(findings.c.id == id)
    return await database.fetch_one(query)

async def add_finding(fd: models.FindingCreate):
    tfd = fd.dict()
    query = findings.insert().values(tfd)
    return await database.execute(query)

async def delete_finding(id: int):
    query = findings.delete().where(findings.c.id == id)
    return await database.execute(query)

async def update_finding(id: int, fd: models.FindingUpdate):
    query = (
        findings
            .update()
            .where(findings.c.id == id)
            .values(**fd.dict())
    )
    return await database.execute(query=query)

