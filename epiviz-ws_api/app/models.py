from typing import List, Optional
from pydantic import BaseModel

class WorkspaceBase(BaseModel):
    workspace_id: str
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


class WorkspaceUpdate(WorkspaceBase):
    workspace_id: Optional[str] = None
    user_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    genomes: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    workspace: Optional[dict] = None
