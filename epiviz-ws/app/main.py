from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

fake_ws_db = [
    {
        'user_id': 'test@example.com',
        'ws_id': 'ws1234',
        'title': 'My workspace',
        'description': 'My description',
        'genomes': ['hg39'],
        'tags': ['atac-seq', 'rna-seq'],
        'ws_def': '{"ws_id": "ws1234", "components": [{"id":"epiviz-wss2jrf", "type":"linetrack"}]}'
    }
]

class Workspace(BaseModel):
    user_id: str
    ws_id: str
    title: Optional[str]
    description: Optional[str]
    genomes: List[str]
    tags: Optional[List[str]]
    ws_def: str

@app.get('/', response_model=List[Workspace])
async def index():
    return fake_ws_db

@app.post('/', status_code=201)
async def add_workspace(payload: Workspace):
    ws = payload.dict()
    fake_ws_db.append(ws)
    return {'id': len(fake_ws_db) - 1}

@app.put('/{id}')
async def update_workspace(id: int, payload: Workspace):
    ws = payload.dict()
    num_ws = len(fake_ws_db)
    if not 0 <= id < num_ws:
        raise HTTPException(status_code=404, detail="Workspace with given id not found")
    fake_ws_db[id] = ws
    return None

@app.delete('/{id}')
async def delete_workspace(id: int):
    num_ws = len(fake_ws_db)
    if not 0 <= id < num_ws:
        raise HTTPException(status_code=404, detail="Workspace with given id not found")
    del fake_ws_db[id]
    return None
