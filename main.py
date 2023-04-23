# main.py
from fastapi import FastAPI, HTTPException, Request, Body, Form, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Any
import modal
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, set_key
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, RedirectResponse

load_dotenv()

from linear_types import Issue, User, IssueLabel
from linear_client import LinearClient
from linear_client import IssueInput, AssignIssueInput, IssueModificationInput, status_reversed

from agents.agent_router import AgentRouter

app = FastAPI(
    title="AutoPM",
    description="Automate your product management",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Production server",
        }
    ],
)
templates = Jinja2Templates(directory="templates")
stub = modal.Stub("form_generator")

agent_router = AgentRouter()

@app.middleware("http")
async def check_setup(request: Request, call_next):
    setup_done = os.environ.get("SETUP_DONE", "false")
    if (
        setup_done
        or request.url.path == "/setup"
        or request.url.path == "/get_setup"
        or request.url.path == "/form_setup"
        or request.url.path == "/favicon.ico"
    ):
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
async def get_sssss(issueId: str) -> Issue:
    response = linear_client.get_issue(issueId)
    return response


class SetupModel(BaseModel):
    linear_api_key: str
    openai_api_key: str
    serpapi_api_key: str
    linear_team_id: str


@app.get("/get_setup", response_class=HTMLResponse)
async def get_setup(request: Request):
    return templates.TemplateResponse("setup_form.html", {"request": request})


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

        # re-run load dotenv to pick up changes
        load_dotenv()

        return {
            "message": "API keys have been added to the .env file and setup is complete"
        }
    else:
        raise HTTPException(status_code=400, detail="API keys are already set")


@app.post("/setup")
async def api_setup(setup_data: SetupModel):
    return await setup(
        setup_data.linear_api_key,
        setup_data.openai_api_key,
        setup_data.serpapi_api_key,
        setup_data.linear_team_id,
    )


@app.post("/form_setup")
async def form_setup(request: Request, setup_data: SetupModel):
    response = await setup(
        setup_data.linear_api_key,
        setup_data.openai_api_key,
        setup_data.serpapi_api_key,
        setup_data.linear_team_id,
    )
    print("response:")
    print(response)

    if response.get("message"):
        return RedirectResponse(
            url="/setup_confirmation", status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return templates.TemplateResponse(
            "setup_form.html",
            {"request": request, "error": "Setup failed. Please try againrr."},
        )


@app.get("/setup_confirmation", response_class=HTMLResponse)
async def setup_confirmation(request: Request):
    return templates.TemplateResponse("setup_confirmation.html", {"request": request})

import json

def append_label_id_by_name(all_labels: List[IssueLabel], current_labels: List[IssueLabel], label_name)-> List[str]:
    label_ids = [i.id for i in current_labels]
    # filter down by name:
    filtered_label_ids = [i.id for i in all_labels if i.name == label_name]
    label_ids.extend(filtered_label_ids)
    return list(set(label_ids))

def remove_label_by_name(labels: List[IssueLabel], label_name)-> List[str]:
    return [i.id for i in labels if i.name != label_name]

@app.post("/webhooks/linear")
async def webhooks_linear(request: Request):
    j = await request.json()
    is_update = j["action"] == "update"
    assignee_changed = "assigneeId" in j.get("updatedFrom", {})
    assigned_to_robot = j["data"].get("assignee", {}).get("name") == "AutoPM Robot"

    # TODO: use something like cachetools here
    all_issue_labels = linear_client.list_issue_labels()

    if all([is_update, assignee_changed, assigned_to_robot]):
        print("assigning to AI")
        issue = await linear_client.get_issue(j["data"]["id"])

        prior_state = status_reversed.get(issue.state.id, "todo")

        lables = []
        if issue.labels:
            lables = issue.labels.nodes
        label_ids = append_label_id_by_name(all_issue_labels, lables, "Running")
        await linear_client.update_issue(j["data"]["id"], IssueModificationInput(state="in_progress"))
        print("set new labels:", await linear_client.update_issue(j["data"]["id"], IssueModificationInput(label_ids=label_ids)))

        print("ROUTER START!")
        result = await agent_router.accomplish_issue(issue)
        print("ROUTER END!")

        if result:
            await linear_client.update_issue(j["data"]["id"], IssueModificationInput(
                description=result,
                state="in_review",
                label_ids=remove_label_by_name(lables, "Running"),
            ))
        else:
            await linear_client.update_issue(j["data"]["id"], IssueModificationInput(
                state=prior_state,
                label_ids=remove_label_by_name(lables, "Running")))
        print(await linear_client.assign_issue(j["data"]["id"], None))

    else:
        print("ignoring webhook")
        print({"is_update": is_update, "assignee_changed": assignee_changed, "assigned_to_robot": assigned_to_robot})

    return "ok"


@app.post("/issues/{issue_id}/assign", response_model=Issue)
async def assign_issue(input: AssignIssueInput):
    response = await linear_client.assign_issue(input.issue_id, input.assignee_id)
    return response


@app.get("/users/", response_model=List[User])
async def list_users():
    response = linear_client.list_users()
    return response


@app.get("/issue_labels", response_model=List[IssueLabel])
async def list_issue_labels():
    response = linear_client.list_issue_labels()
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
