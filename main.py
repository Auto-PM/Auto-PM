# main.py
from fastapi import FastAPI, HTTPException, Request, Body, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import modal
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, set_key
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from linear_client import LinearClient
from linear_client import IssueInput, AssignIssueInput, IssueModificationInput, status_reversed
# Project types:
from linear_client import ProjectInput, DocumentInput
from linear_types import Issue, User, IssueLabel, Project, Document
from linear_types import ProjectMilestone, ProjectMilestoneInput

from agents.agent_router import AgentRouter

load_dotenv()

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

linear_client = LinearClient(endpoint="https://api.linear.app/graphql")
agent_router = AgentRouter(agent_kwargs={
    "linear_client": linear_client,
})

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


class Task(BaseModel):
    name: str
    description: Optional[str] = None


@app.get("/issues/", response_model=List[Issue], response_model_exclude_none=True)
async def list_issues(project_id: str):
    filters = {}
    if project_id:
        filters["project"] = {"id": {"eq": project_id}}
    response = await linear_client.list_issues(**filters)
    return response


@app.post("/issues/", response_model=Issue, response_model_exclude_none=True)
async def create_issue(issue: IssueInput):
    response = await linear_client.create_issue(issue)
    return response


@app.post("/issues/bulk/", response_model=List[Issue], response_model_exclude_none=True)
async def create_issue_bulk(issues: List[IssueInput] = Body(..., embed=True)):
    response = []
    for issue in issues:
        print("creating issue:", issue)
        response += [await linear_client.create_issue(issue)]
        print("response:", response)
    return response


@app.post("/issues/{issue_id}/", response_model=Issue, response_model_exclude_none=True)
async def patch_issue(issue_id: str, issue: IssueModificationInput):
    response = await linear_client.update_issue(issue_id, issue)
    return response


@app.get("/issues/{issueId}", response_model=Issue, response_model_exclude_none=True)
async def get_issue(issueId: str) -> Issue:
    response = linear_client.get_issue(issueId)
    return response


@app.delete("/issues/{issueId}", response_model=Issue, response_model_exclude_none=True)
async def delete_issue(issueId: str) -> Issue:
    response = await linear_client.delete_issue(issueId)
    return response


class SetupModel(BaseModel):
    linear_api_key: str
    openai_api_key: str
    serpapi_api_key: str
    linear_team_id: str


@app.get("/get_setup", response_class=HTMLResponse, response_model_exclude_none=True)
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


def append_label_id_by_name(all_labels: List[IssueLabel], current_labels: List[IssueLabel], label_name)-> List[str]:
    label_ids = [i.id for i in current_labels]
    # filter down by name:
    filtered_label_ids = [i.id for i in all_labels if i.name == label_name]
    label_ids.extend(filtered_label_ids)
    return list(set(label_ids))

def remove_label_by_name(labels: List[IssueLabel], label_name)-> List[str]:
    return [i.id for i in labels if i.name != label_name]

all_issue_labels = linear_client.list_issue_labels()

@app.post("/webhooks/linear")
async def webhooks_linear(request: Request):
    j = await request.json()

    is_update = j["action"] == "update"
    assignee_changed = "assigneeId" in j.get("updatedFrom", {})
    assigned_to_robot = j["data"].get("assignee", {}).get("name") == "AutoPM Robot"
    status_changed = "stateId" in j.get("updatedFrom", {})

    updated_to = j.get("data", {}).get("state")

    if type(updated_to) == str:
        return

    updated_to_friendly = status_reversed.get(updated_to.get("id"), None)
    issue_placed_in_review = updated_to_friendly == "in_review"

    # TODO: use something like cachetools here
    # all_issue_labels = linear_client.list_issue_labels()

    if all([is_update, assignee_changed, assigned_to_robot]):
        print("Assigning to AI")
        issue = await linear_client.get_issue(j["data"]["id"])

        prior_state = status_reversed.get(issue.state.id, "todo")

        lables = []
        if issue.labels:
            lables = issue.labels.nodes
        label_ids = append_label_id_by_name(all_issue_labels, lables, "Running")
        await linear_client.update_issue(j["data"]["id"], IssueModificationInput(state="in_progress"))
        print("set new labels:", await linear_client.update_issue(
            j["data"]["id"],
            IssueModificationInput(label_ids=label_ids),
        ))

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

    elif all([is_update, status_changed, issue_placed_in_review]):
        print("considering issue evaluator")
        issue = await linear_client.get_issue(j["data"]["id"])

        child_issues = []
        if issue.parent:
            child_issues = await linear_client.list_issues(
                        parent={"id":{"eq": issue.parent.id}},
            )

        child_issues = [{"title": i.title, "status": i.state.name} for i in child_issues if i.id != issue.id]

        lables = []
        if issue.labels:
            lables = issue.labels.nodes
        label_ids = append_label_id_by_name(all_issue_labels, lables, "Evaluating")
        print("set new labels:", await linear_client.update_issue(
            j["data"]["id"],
            IssueModificationInput(label_ids=label_ids),
            ))
        eval_result = await agent_router.evaluate_issue_completion(issue, child_issues)
        if eval_result:
            await linear_client.update_issue(j["data"]["id"], IssueModificationInput(
                state="done",
                label_ids=remove_label_by_name(lables, "Evaluating"),
            ))
        else:
            await linear_client.update_issue(j["data"]["id"], IssueModificationInput(
                label_ids=remove_label_by_name(lables, "Evaluating"),
            ))
        print("eval result:", eval_result)
    return "ok"


@app.post("/issues/{issue_id}/assign", response_model=Issue, response_model_exclude_none=True)
async def assign_issue(input: AssignIssueInput):
    """Assign an issue to a user"""
    response = await linear_client.assign_issue(input.issue_id, input.assignee_id)
    return response


@app.get("/users/", response_model=List[User], response_model_exclude_none=True)
async def list_users() -> List[User]:
    """List all users"""
    response = linear_client.list_users()
    return response


@app.get("/issue_labels", response_model=List[IssueLabel], response_model_exclude_none=True)
async def list_issue_labels() -> List[IssueLabel]:
    """List all issue labels"""
    response = linear_client.list_issue_labels()
    return response


@app.get("/projects", response_model=List[Project], response_model_exclude_none=True)
async def list_projects() -> List[Project]:
    """List all projects"""
    response = await linear_client.list_projects()
    return response


@app.get("/projects/{project_id}", response_model=Project, response_model_exclude_none=True)
async def get_project(project_id: str) -> Project:
    """Get a project by ID"""
    response = await linear_client.get_project(project_id)
    return response


@app.post("/projects", response_model=Project, response_model_exclude_none=True)
async def create_project(input: ProjectInput) -> Project:
    """Create a project"""
    response = await linear_client.create_project(input)
    return response 


@app.post("/projects/{project_id}", response_model=Project, response_model_exclude_none=True)
async def update_project(project_id: str, input: ProjectInput) -> Project:
    """Update a project"""
    response = await linear_client.update_project(project_id, input)
    return response


@app.delete("/projects/{project_id}", response_model=Project, response_model_exclude_none=True)
async def delete_project(project_id: str) -> Project:
    """Delete a project"""
    response = await linear_client.delete_project(project_id)
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

# project document endpoints
@app.get("/projects/{project_id}/documents", response_model=List[Document], response_model_exclude_none=True)
async def list_documents(project_id: str) -> List[Document]:
    """List all documents (AKA product specifications)."""
    response = await linear_client.list_documents(project_id)
    return response

@app.get("/projects/{project_id}/documents/{document_id}", response_model=Document, response_model_exclude_none=True)
async def get_document(project_id: str, document_id: str) -> Document:
    """Get a document by ID"""
    response = await linear_client.get_document(document_id)
    return response

@app.post("/projects/{project_id}/documents", response_model=Document, response_model_exclude_none=True)
async def create_document(project_id: str, input: DocumentInput) -> Document:
    """Create a document"""
    response = await linear_client.create_document(project_id, input)
    return response

@app.post("/projects/{project_id}/documents/{document_id}", response_model=Document, response_model_exclude_none=True)
async def update_document(project_id: str, document_id: str, input: DocumentInput) -> Document:
    """Update a document"""
    response = await linear_client.update_document(project_id, document_id, input)
    return response

@app.delete("/projects/{project_id}/documents/{document_id}", response_model=Document, response_model_exclude_none=True)
async def delete_document(project_id: str, document_id: str) -> bool:
    """Delete a document"""
    response = await linear_client.delete_document(project_id, document_id)
    return response


# project milestone endpoints
@app.get("/projects/{project_id}/milestones", response_model=List[ProjectMilestone], response_model_exclude_none=True)
async def list_milestones(project_id: str) -> List[ProjectMilestone]:
    """List all milestones."""
    response = await linear_client.list_milestones(project_id)
    return response

@app.get("/projects/{project_id}/milestones/{milestone_id}",
         response_model=ProjectMilestone, response_model_exclude_none=True)
async def get_milestone(project_id: str, milestone_id: str) -> ProjectMilestone:
    """Get a milestone by ID"""
    response = await linear_client.get_milestone(milestone_id)
    return response

@app.post("/projects/{project_id}/milestones", response_model=ProjectMilestone, response_model_exclude_none=True)
async def create_milestone(project_id: str, input: ProjectMilestoneInput) -> ProjectMilestone:
    """Create a milestone"""
    response = await linear_client.create_milestone(project_id, input)
    return response

@app.post("/projects/{project_id}/milestones/{milestone_id}",
          response_model=ProjectMilestone, response_model_exclude_none=True)
async def update_milestone(project_id: str, milestone_id: str, input: ProjectMilestoneInput) -> ProjectMilestone:
    """Update a milestone"""
    response = await linear_client.update_milestone(milestone_id, input)
    return response

@app.delete("/projects/{project_id}/milestones/{milestone_id}", 
            response_model=ProjectMilestone, response_model_exclude_none=True)
async def delete_milestone(project_id: str, milestone_id: str) -> bool:
    """Delete a milestone"""
    response = await linear_client.delete_milestone(milestone_id)
    return response

@stub.asgi(image=image, mounts=[template_mount, asset_mount])
def fastapi_app():
    return app
