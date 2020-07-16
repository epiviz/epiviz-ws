from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class Workspace(BaseModel):
    user_id: str
    ws_id: str
    title: Optional[str]
    description: Optional[str]
    genomes: List[str]
    tags: Optional[List[str]]
    ws_def: str

