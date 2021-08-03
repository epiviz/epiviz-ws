from typing import List, Optional
from datetime import datetime
from fastapi import Header, APIRouter, Depends, HTTPException

from app import models
from app import db_manager
from app.auth import get_user_from_header

findings = APIRouter()

@findings.get('/', response_model=List[models.Finding])
async def index():
    return await db_manager.get_all_findings()

@findings.get('/user/{user_id}', response_model=List[models.Finding])
async def get_user_findings(user_id: str, user: models.User = Depends(get_user_from_header)):
    if user_id == user.username:
        return await db_manager.get_user_findings(user_id)
    else: 
        raise HTTPException(status_code=404, detail="UnixID does not match token")

@findings.get('/{id}', response_model=models.Finding)
async def get_finding(id: int):
    return await db_manager.get_finding(id)

@findings.post('/', response_model=models.Finding)
async def add_finding(payload: models.FindingCreate):
    id = await db_manager.add_finding(payload)
    response = {
        'id': id,
        **payload.dict()
    }

    return response

@findings.put('/{id}')
async def update_finding(id: int, payload: models.FindingUpdate, user: models.User = Depends(get_user_from_header)):
    fd = await db_manager.get_finding(id)
    if not fd:
        raise HTTPException(status_code=404, detail="Finding not found")

    if fd.get("user_id") == user.username or "admin" in user.roles:
        update_data = payload.dict(exclude_unset=True)
        fd_in_db = models.findingUpdate(**fd)
        updated_fd = fd_in_db.copy(update=update_data)
        return await db_manager.update_finding(id, updated_fd)    
    else:
        raise HTTPException(status_code=404, detail="UnixID does not match token")

@findings.delete('/{id}')
async def delete_finding(id: int, user: models.User = Depends(get_user_from_header)):
    fd = await db_manager.get_finding(id)
    if not fd:
        raise HTTPException(status_code=404, detail="finding not found")
    
    if fd.get("user_id") == user.username:
        return await db_manager.delete_finding(id)
    else:
        raise HTTPException(status_code=404, detail="UnixID does not match token")
