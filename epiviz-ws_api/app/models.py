from typing import List, Optional
from pydantic import BaseModel

class WorkspaceBase(BaseModel):
    user_id: str
    title: Optional[str]
    description: Optional[str]
    genomes: Optional[List[str]]
    tags: Optional[List[str]]
    workspace: dict

class WorkspaceCreate(WorkspaceBase):
    pass

class Workspace(WorkspaceBase):
    id: int
    workspace_uuid: Optional[str]

class WorkspaceUpdate(WorkspaceBase):
    user_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    genomes: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    workspace: Optional[dict] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    roles: Optional[List[str]] = None