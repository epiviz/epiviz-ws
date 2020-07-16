from typing import List, Optional
from datetime import datetime
from fastapi import Header, APIRouter

from app import models
from app import db_manager

workspaces = APIRouter()

@workspaces.get('/', response_model=List[models.Workspace])
async def index():
    return await db_manager.get_all_workspaces()

@workspaces.get('/{workspace_id}', response_model=models.Workspace)
async def get_workspace(workspace_id: str):
    return await db_manager.get_workspace(workspace_id)

@workspaces.post('/', status_code=201)
async def add_workspace(payload: models.WorkspaceCreate):
    id = await db_manager.add_workspace(payload)
    response = {
        'id': id,
        **payload.dict()
    }

    return response

@workspaces.put('/{workspace_id}')
async def update_workspace(workspace_id: str, payload: models.WorkspaceUpdate):
    ws = await db_manager.get_workspace(workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")

    update_data = payload.dict(exclude_unset=True)
    ws_in_db = models.WorkspaceUpdate(**ws)
    updated_ws = ws_in_db.copy(update=update_data)
    return await db_manager.update_workspace(workspace_id, updated_ws)

@workspaces.delete('/{workspace_id}')
async def delete_workspace(workspace_id: str):
    ws = await db_manager.get_workspace(workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return await db_manager.delete_workspace(workspace_id)
