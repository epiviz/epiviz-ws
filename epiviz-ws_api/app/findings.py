from typing import List, Optional
from datetime import datetime
from fastapi import Header, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models, db_manager
from app.auth import get_user_from_header
from app.db.db_session import get_db

findings = APIRouter()

@findings.get('/', response_model=List[models.Finding])
async def index(db: Session = Depends(get_db)):
    return await db_manager.get_all_findings(db)

@findings.get('/{id}', response_model=models.Finding)
async def get_finding(id: int,
    db: Session = Depends(get_db)):
    return await db_manager.get_finding(db, id)

@findings.post('/', response_model=models.Finding)
async def add_Finding(payload: models.FindingCreate,
    db: Session = Depends(get_db)):

    ws = await db_manager.get_workspace(db, payload.workspace_id)

    if not ws:
        raise HTTPException(status_code=404, detail=f"Cannot find Workspace: {payload.workspace_id}")

    return await db_manager.add_finding(db, payload)

@findings.put('/{id}')
async def update_finding(id: int, payload: models.FindingUpdate, 
    user: models.User = Depends(get_user_from_header),
    db: Session = Depends(get_db)):
    ws = await db_manager.get_finding(db, id)
    if not ws:
        raise HTTPException(status_code=404, detail="Finding not found")

    if ws.get("user_id") == user.username:
        update_data = payload.dict(exclude_unset=True)
        return await db_manager.update_finding(db, id, update_data)    
    else:
        raise HTTPException(status_code=404, detail="UnixID does not match token")

@findings.delete('/{id}')
async def delete_finding(id: int, 
    user: models.User = Depends(get_user_from_header),
    db: Session = Depends(get_db)):
    ws = await db_manager.get_finding(db, id)
    if not ws:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    if ws.get("user_id") == user.username:
        return await db_manager.delete_finding(db, id)
    else:
        raise HTTPException(status_code=404, detail="UnixID does not match token")
