from sqlalchemy.orm import Session

from app.db import schema, models
from uuid import uuid4

async def get_all_workspaces(db: Session):
    return db.query(schema.Workspace).all()

async def get_user_workspaces(db: Session, user_id: str):
    return db.query(schema.Workspace).filter(
        schema.Workspace.user_id == user_id
    ).all()

async def get_workspace_tag(db: Session, tag: str):
    return db.query(schema.Workspace).filter(
        schema.Workspace.tags.any(tag)
    ).all()

async def get_workspace(db: Session, id: int):
    return db.query(schema.Workspace).filter(
        schema.Workspace.id == id
    ).first()

async def get_workspace_uuid(db: Session, uuid: str):
    return db.query(schema.Workspace).filter(
        schema.Workspace.workspace_uuid == uuid
    ).first()

async def add_workspace(db: Session, ws: models.WorkspaceCreate):
    wks = schema.Workspace(**ws.dict())
    # flag_modified(wks, 'user_list')
    wks.workspace_uuid = str(uuid4()).split("-")[0]

    db.add(wks)
    db.commit()
    db.refresh(wks)

    return wks

async def delete_workspace(db: Session, id: int):
    current_ws = await get_workspace(db, id)
    
    db.delete(current_ws)
    db.commit()   

    return current_ws

async def update_workspace(db: Session, id: int, ws: models.WorkspaceUpdate):
    current_ws = await get_workspace(db, id)
    
    #  update attributes
    for key, value in ws.items():
        setattr(current_ws, key, value)
    
    db.add(current_ws)
    db.commit()
    db.refresh(current_ws)
    
    return current_ws

async def get_all_findings(db: Session):
    return db.query(schema.Finding).all()

async def get_finding(db: Session, id: int):
    return db.query(schema.Finding).filter(
        schema.Finding.id == id
    ).first()

async def add_finding(db: Session, ws: models.Finding):
    fds = schema.Finding(**ws.dict())

    db.add(fds)
    db.commit()
    db.refresh(fds)

    return fds

async def delete_finding(db: Session, id: int):
    current_fds = await get_workspace(db, id)
    
    db.delete(current_fds)
    db.commit()   

    return current_fds

async def update_finding(db: Session, id: int, ws: models.FindingUpdate):
    current_fds = await get_workspace(db, id)
    
    #  update attributes
    for key, value in ws.items():
        setattr(current_fds, key, value)
    
    db.add(current_fds)
    db.commit()
    db.refresh(current_fds)
    
    return current_fds