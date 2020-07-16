from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def index():
    return { "Epiviz": "Workspaces" }