from typing import List, Optional
from datetime import datetime
from fastapi import Header, APIRouter, Depends, HTTPException

from app import models
from app import db_manager
from app.auth import get_user_from_header

workspaces = APIRouter()

@workspaces.get('/', response_model=List[models.Workspace])
async def index():
    return await db_manager.get_all_workspaces()

@workspaces.get('/user/{user_id}', response_model=List[models.Workspace])
async def get_user_workspaces(user_id: str, user: models.User = Depends(get_user_from_header)):
    if user_id == user.username:
        return await db_manager.get_user_workspaces(user_id)
    else: 
        raise HTTPException(status_code=404, detail="UnixID does not match token")

@workspaces.get('/{id}', response_model=models.Workspace)
async def get_workspace(id: int):
    return await db_manager.get_workspace(id)

@workspaces.get('/uuid/{uuid}', response_model=models.Workspace)
async def get_workspace_uuid(uuid: str):
    return await db_manager.get_workspace_uuid(uuid)

@workspaces.post('/', status_code=201)
async def add_workspace(payload: models.WorkspaceCreate):
    print("in add workspace")
    id = await db_manager.add_workspace(payload)
    print("after db add workspace")
    print(id)
    response = {
        'id': id,
        **payload.dict()
    }

    return response

@workspaces.put('/{id}')
async def update_workspace(id: int, payload: models.WorkspaceUpdate, user: models.User = Depends(get_user_from_header)):
    ws = await db_manager.get_workspace(id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")

    if ws.get("user_id") == user.username:
        update_data = payload.dict(exclude_unset=True)
        ws_in_db = models.WorkspaceUpdate(**ws)
        updated_ws = ws_in_db.copy(update=update_data)
        return await db_manager.update_workspace(id, updated_ws)    
    else:
        raise HTTPException(status_code=404, detail="UnixID does not match token")

@workspaces.delete('/{id}')
async def delete_workspace(id: int, user: models.User = Depends(get_user_from_header)):
    ws = await db_manager.get_workspace(id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    if ws.get("user_id") == user.username:
        return await db_manager.delete_workspace(id)
    else:
        raise HTTPException(status_code=404, detail="UnixID does not match token")
