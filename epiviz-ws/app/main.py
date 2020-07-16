from fastapi import FastAPI

from app.api.workspaces import workspaces

app = FastAPI()
app.include_router(workspaces)


