# main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import modal
from fastapi.middleware.cors import CORSMiddleware

from linear_types import Issue, WorkflowState
from linear_client import LinearClient

app = FastAPI()
stub = modal.Stub("form_generator")

app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
origins = [
    "https://chat.openai.com",
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

linear_client = LinearClient(endpoint="https://api.linear.app/graphql")


class Task(BaseModel):
    name: str
    description: Optional[str] = None


from linear_client import IssueInput, ListIssueFilter


@app.get("/issues/", response_model=List[Issue])
async def list_issues(stateId: str | None = None):
    filter = {}
    if stateId:
        filter["stateId"] = stateId
    response = linear_client.list_issues(filter)
    return response

@app.get("/issues/{issueId}", response_model=Issue)
async def get_issue(issueId: str):
    """Look up details for a specific issue."""
    response = linear_client.get_issue(issueId)
    return response


@app.post("/issues/", response_model=Issue)
async def create_issue(issue: IssueInput):
    response = linear_client.create_issue(issue)
    return response


@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task_id = len(tasks) + 1
    tasks[task_id] = task
    return task


@app.post("/tasks/{task_id}/delete")
async def delete_task(task_id: str):
    response = linear_client.delete_issue(task_id)
    return response


@app.get("/tasks/", response_model=List[Task])
async def read_tasks(skip: int = 0, limit: int = 10):
    return list(tasks.values())[skip : skip + limit]

@app.patch("/issues/{issue_id}", response_model=Issue)
async def patch_issue(issue_id: str, issue: IssueInput):
    response = linear_client.update_issue(issue_id, issue)
    return response


# Workflow States
@app.get("/workflow_states/", response_model=List[WorkflowState])
async def list_workflow_states():
    """Lists workflow states (such as Done, or Backlog). Also known as issue states."""
    response = linear_client.list_workflow_states()
    return response

# Create a custom image with the required dependencies installed
# image = modal.Image.debian_slim().pip_install()
image = modal.Image.debian_slim().pip_install()
template_mount = modal.Mount.from_local_file(
    ".well-known/ai-plugin.json", remote_path="/root/.well-known/ai-plugin.json"
)
asset_mount = modal.Mount.from_local_file(
    "assets/logo.png", remote_path="/root/assets/logo.png"
)


@stub.asgi(image=image, mounts=[template_mount, asset_mount])
def fastapi_app():
    return app


# @app.post("/items/", response_model=Item)
# async def create_item(item: Item):
#     item_id = len(items) + 1
#     items[item_id] = item
#     return item


# @app.get("/items/", response_model=List[Item])
# async def read_items(skip: int = 0, limit: int = 10):
#     return list(items.values())[skip : skip + limit]


# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: int):
#     item = items.get(item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item


# @app.put("/items/{item_id}", response_model=Item)
# async def update_item(item_id: int, item: Item):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     items[item_id] = item
#     return item


# @app.delete("/items/{item_id}", response_model=Item)
# async def delete_item(item_id: int):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     item = items.pop(item_id)
#     return item
