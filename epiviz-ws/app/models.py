from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class WorkspaceIn(BaseModel):
    user_id: str
    title: Optional[str]
    description: Optional[str]
    genomes: List[str]
    tags: Optional[List[str]]
    ws_def: str

class WorkspaceOut(WorkspaceIn):
    ws_id: int

class WorkspaceUpdate(WorkspaceIn):
    title: Optional[str] = None
    description: Optional[str] = None
    genomes: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    ws_def: Optional[str] = None
