from typing import List, Optional
from datetime import datetime
from fastapi import Header, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models, db_manager
from app.auth import get_user_from_header
from app.db.db_session import get_db

workspaces = APIRouter()

@workspaces.get('/', response_model=List[models.Workspace])
async def index(db: Session = Depends(get_db)):
    return await db_manager.get_all_workspaces(db)

@workspaces.get('/user/{user_id}', response_model=List[models.Workspace])
async def get_user_workspaces(user_id: str, 
    user: models.User = Depends(get_user_from_header),
    db: Session = Depends(get_db)):
    if user_id == user.username:
        return await db_manager.get_user_workspaces(db, user_id)
    else: 
        raise HTTPException(status_code=404, detail="UnixID does not match token")

@workspaces.get('/{id}', response_model=models.Workspace)
async def get_workspace(id: int,
    db: Session = Depends(get_db)):
    return await db_manager.get_workspace(db, id)

@workspaces.get('/{id}/findings', response_model=List[models.Finding])
async def get_workspace_findings(id: int,
    db: Session = Depends(get_db)):

    current_ws =  await db_manager.get_workspace(db, id)
    return current_ws.findings

@workspaces.get('/uuid/{uuid}', response_model=models.Workspace)
async def get_workspace_uuid(uuid: str,
    db: Session = Depends(get_db)):
    return await db_manager.get_workspace_uuid(db, uuid)

@workspaces.get('/uuid/{uuid}/findings', response_model=List[models.Finding])
async def get_workspace_uuid(uuid: str,
    db: Session = Depends(get_db)):
    current_ws = await db_manager.get_workspace_uuid(db, uuid)

    return current_ws.findings

@workspaces.get('/tag/{tag}', response_model=List[models.Workspace])
async def get_workspace_tag(tag: str,
    db: Session = Depends(get_db)):
    return await db_manager.get_workspace_tag(db, tag)

@workspaces.post('/', response_model=models.Workspace)
async def add_workspace(payload: models.WorkspaceCreate,
    db: Session = Depends(get_db)):
    return await db_manager.add_workspace(db, payload)

@workspaces.put('/{id}')
async def update_workspace(id: int, payload: models.WorkspaceUpdate, 
    user: models.User = Depends(get_user_from_header),
    db: Session = Depends(get_db)):

    ws = await db_manager.get_workspace(db, id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")

    if ws.get("user_id") == user.username:
        update_data = payload.dict(exclude_unset=True)
        return await db_manager.update_workspace(db, id, update_data)    
    else:
        raise HTTPException(status_code=404, detail="UnixID does not match token")

@workspaces.delete('/{id}')
async def delete_workspace(id: int, 
    user: models.User = Depends(get_user_from_header),
    db: Session = Depends(get_db)):
    ws = await db_manager.get_workspace(db, id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    if ws.get("user_id") == user.username:
        return await db_manager.delete_workspace(db, id)
    else:
        raise HTTPException(status_code=404, detail="UnixID does not match token")
