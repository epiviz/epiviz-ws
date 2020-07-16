from typing import List, Optional
from datetime import datetime
from fastapi import Header, APIRouter

from app.api.models import WorkspaceIn, WorkspaceOut
from app.api import db_manager

workspaces = APIRouter()

@workspaces.get('/', response_model=List[WorkspaceOut])
async def index():
    return await db_manager.get_all_workspaces()

@workspaces.post('/', status_code=201)
async def add_workspace(payload: WorkspaceIn):
    ws_id = await db_manager.add_workspace(payload)
    response = {
        'ws_id': ws_id,
        **payload.dict()
    }

    return response

@workspaces.put('/{ws_id}')
async def update_workspace(ws_id: int, payload: WorkspaceIn):
    ws = await db_manager.get_workspace(ws_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")

    update_data = payload.dict(exclude_unset=True)
    ws_in_db = WorkspaceIn(**ws)
    updated_ws = ws_in_db.copy(update=update_data)
    return await db_manager.update_workspace(ws_id, updated_ws)

@workspaces.delete('/{ws_id}')
async def delete_workspace(ws_id: int):
    ws = await db_manager.get_workspace(ws_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return await db_manager.delete_workspace(ws_id)
