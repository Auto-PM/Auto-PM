# main.py
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Any
import modal
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, set_key
import os


load_dotenv()

from linear_types import Issue, User
from linear_client import LinearClient
from linear_client import IssueInput, AssignIssueInput, IssueModificationInput

app = FastAPI(
    title="AutoPM",
    version="0.0.1",
    servers=[
        {"url": "http://localhost:8000", "description": "Production environment"},
    ],
)
stub = modal.Stub("form_generator")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    setup_done = os.environ.get("SETUP_DONE", "false")
    print("setup_done:", setup_done)
    if not setup_done or request.url.path == "/setup":
        response = await call_next(request)
    else:
        print("setup not done, returning 403")
        raise HTTPException(status_code=403, detail="Forbidden")
    return response


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


@app.get("/issues/", response_model=List[Issue])
async def list_issues():
    response = linear_client.list_issues()
    return response


@app.post("/issues/", response_model=Issue)
async def create_issue(issue: IssueInput):
    response = linear_client.create_issue(issue)
    return response


@app.post("/issues/bulk/", response_model=List[Issue])
async def create_issue(issues: List[IssueInput] = Body(..., embed=True)):
    response = []
    for issue in issues:
        print("creating issue:", issue)
        response += [linear_client.create_issue(issue)]
        print("response:", response)
    return response


@app.post("/issues/{issue_id}/", response_model=Issue)
async def patch_issue(issue_id: str, issue: IssueModificationInput):
    response = linear_client.update_issue(issue_id, issue)
    return response


@app.get("/issues/{issueId}", response_model=Issue)
async def get_issue(issueId: str):
    response = linear_client.get_issue(issueId)
    return response


@app.post("/setup")
async def setup(
    linear_api_key: str, openai_api_key: str, serpapi_api_key: str, linear_team_id: str
):
    if not os.environ.get("SETUP_DONE", "false") == "true":
        # Check if the .env file exists, if not, create one
        if not os.path.exists(".env"):
            with open(".env", "w") as env_file:
                env_file.write("")

        set_key(".env", "LINEAR_API_KEY", linear_api_key)
        set_key(".env", "OPENAI_API_KEY", openai_api_key)
        set_key(".env", "LINEAR_TEAM_ID", linear_team_id)
        set_key(".env", "SERPAPI_API_KEY", serpapi_api_key)
        set_key(".env", "SETUP_DONE", "true")

        os.environ["SETUP_DONE"] = "true"

        return {
            "message": "API keys have been added to the .env file and setup is complete"
        }
    else:
        raise HTTPException(status_code=400, detail="API keys are already set")


import json
from agents.llm import accomplish_issue


@app.post("/webhooks/linear")
async def webhooks_linear(request: Request):
    j = await request.json()
    print("webhook payload:")
    print(json.dumps(j))
    print("action:", j["action"])
    print("data:", j["data"])
    if (
        j["action"] == "update"
        and j["data"].get("assignee", {}).get("name") == "AutoPM Robot"
        and "assigneeId" in j["updatedFrom"]
    ):
        print("assigning to AI")
        issue_description = j["data"]["title"]

        if j["data"].get("description"):
            issue_description += "\n\nDescription:" + j["data"]["description"]
            issue_description = (
                j["data"]["description"]
                + "\n\n-------\n\n"
                + accomplish_issue(issue_description)
            )
        else:
            issue_description = accomplish_issue(issue_description)
        print("issue_description:", issue_description)
        linear_client.update_issue(
            j["data"]["id"],
            IssueModificationInput(
                description=issue_description,
                state="in_review",
            ),
        )

    return "ok"


@app.post("/issues/{issue_id}/assign", response_model=Issue)
async def assign_issue(input: AssignIssueInput):
    print("assign")
    response = linear_client.assign_issue(input.issue_id, input.assignee_id)
    return response


@app.get("/users/", response_model=List[User])
async def list_users():
    response = linear_client.list_users()
    return response


# Create a custom image with the required dependencies installed
# image = modal.Image.debian_slim().pip_install()
image = modal.Image.debian_slim().pip_install("requests")
template_mount = modal.Mount.from_local_file(
    ".well-known/ai-plugin.json", remote_path="/root/.well-known/ai-plugin.json"
)
asset_mount = modal.Mount.from_local_file(
    "assets/logo.png", remote_path="/root/assets/logo.png"
)


@stub.asgi(image=image, mounts=[template_mount, asset_mount])
def fastapi_app():
    return app
