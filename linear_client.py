import os
from typing import List, Optional
import requests
import json
from enum import Enum
from typing import Any

import httpx
from pydantic import BaseModel, Field, Json
from pydantic import constr

from linear_types import Issue, User, IssueLabel, Project, Document
from linear_graphql_queries import QUERIES


# TODO: don't hardcode these
status = {
    "in_review": "7c0bbc28-ffce-45b4-b432-d9223c2330a9",
    "in_progress": "f4bf4bfa-7a53-4b9c-8a5f-6efd2167afd4",
    "cancelled": "ab54a373-3661-44f8-9cb8-c464fab63bc6",
    "done": "09e6c51b-8ff9-4c5a-a797-4afd3cae9fa1",
    "backlog": "15645ccf-4883-48fb-9483-d194b9cb19a1",
    "todo": "4781c172-be3b-43fd-9db1-55924c2d46d8",
}
status_reversed = {v: k for k, v in status.items()}


class LinearError(Exception):
    pass

class IssueState(Enum):
    IN_REVIEW = "in_review"
    IN_PROGRESS = "in_progress"
    CANCELLED = "cancelled"
    DONE = "done"
    BACKLOG = "backlog"
    TODO = "todo"

    def state_id(self) -> Any:
        return status[self.name.lower()]


class IssueInput(BaseModel):
    parent_id: Optional[str] = None
    project_id: Optional[str] = None
    title: str
    description: str
    priority: Optional[float]
    state: IssueState = Field(
        ...,
        description="Issue state/status. The current status of the issue. If a user asks to mark an issue a \
        certain status you should not mention it anywhere in the title or description but instead just mark it \
        here in 'state'. (accepted values: 'in_review', 'in_progress', 'todo', 'done', 'backlog', 'cancelled')",
        example=IssueState.IN_REVIEW,
    )
    label_ids: Optional[List[str]] = None


class AssignIssueInput(BaseModel):
    issue_id: str
    assignee_id: str


class IssueModificationInput(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[float] = None
    state: Optional[IssueState] = Field(
        None,
        description="Issue state/status. The current status of the issue. (accepted values: \
                'in_review', 'in_progress', 'todo', 'done', 'backlog', 'cancelled')",
        example=IssueState.IN_REVIEW,
    )
    label_ids: Optional[List[str]] = None


class ProjectInput(BaseModel):
    name: str
    description: constr(max_length=250)
    priority: Optional[float]
    state: IssueState = Field(
        ...,
        description="Issue state/status. The current status of the issue. If a user asks to mark an issue a \
        certain status you should not mention it anywhere in the title or description but instead just mark it \
        here in 'state'. (accepted values: 'in_review', 'in_progress', 'todo', 'done', 'backlog', 'cancelled')",
        example=IssueState.IN_REVIEW,
    )
    label_ids: Optional[List[str]] = None


class DocumentInput(BaseModel):
    # project_id: str
    title: str
    content: str
    content_data: Optional[Json] = None


class LinearClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()

    def _get_api_key_and_team_id(self):
        LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY", "")
        LINEAR_TEAM_ID = os.environ.get("LINEAR_TEAM_ID", "")
        return LINEAR_API_KEY, LINEAR_TEAM_ID

    def _run_graphql_query(self, query, variables=None):
        LINEAR_API_KEY, LINEAR_TEAM_ID = self._get_api_key_and_team_id()
        print("variables:", json.dumps(variables))
        return self.session.post(
            self.endpoint,
            json={
                "query": query,
                "variables": variables or {},
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LINEAR_API_KEY}",
            },
        ).json()

    async def _arun_graphql_query(self, query, variables=None):
        LINEAR_API_KEY, LINEAR_TEAM_ID = self._get_api_key_and_team_id()
        #print("variables:", json.dumps(variables))
        async with httpx.AsyncClient() as client:
            r = await client.post(
                self.endpoint,
                json={
                    "query": query,
                    "variables": variables or {},
                },
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {LINEAR_API_KEY}",
                },
            )
        return r.json()

    async def list_issues(self, **kwargs):
        LINEAR_API_KEY, LINEAR_TEAM_ID = self._get_api_key_and_team_id()
        variables={
            "filter": {
                "team": {
                    "id": {
                        "eq": LINEAR_TEAM_ID,
                    }
                },
            }
        }
        for k,v in kwargs.items():
            variables["filter"][k] = v
        result = await self._arun_graphql_query(
            QUERIES["list_issues"],
            variables=variables,
        )
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return [Issue(**issue) for issue in result["data"]["issues"]["nodes"]]

    async def create_issue(self, input: IssueInput):
        LINEAR_API_KEY, LINEAR_TEAM_ID = self._get_api_key_and_team_id()
        # TODO(Can we just pass the whole input as variables?)
        variables = {
            "teamId": LINEAR_TEAM_ID,
            "title": input.title,
            "description": input.description,
            "priority": input.priority,
            "stateId": input.state.state_id(),
        }
        if input.parent_id:
            variables["parentId"] = input.parent_id
        if input.project_id:
            variables["projectId"] = input.project_id
        result = await self._arun_graphql_query(QUERIES["create_issue"], variables)
        print("variables:", json.dumps(variables))
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return Issue(**result["data"]["issueCreate"]["issue"])

    def delete_issue(self, issue_id):
        result = self._run_graphql_query(
            QUERIES["delete_issue"],
            variables={
                "issueDeleteId": issue_id,
            },
        )
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return result["data"]["issueDelete"]["success"]

    async def update_issue(self, issue_id, issue: IssueInput):
        LINEAR_API_KEY, LINEAR_TEAM_ID = self._get_api_key_and_team_id()
        variables = {
            "id": issue_id,
            "teamId": LINEAR_TEAM_ID,
        }
        if issue.title is not None:
            variables["title"] = issue.title
        if issue.description is not None:
            variables["description"] = issue.description
        if issue.priority is not None:
            variables["priority"] = issue.priority
        if issue.state is not None:
            variables["stateId"] = issue.state.state_id()
        if issue.label_ids is not None:
            variables["labelIds"] = issue.label_ids
        result = await self._arun_graphql_query(QUERIES["update_issue"], variables)
        print("variables:", json.dumps(variables))
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return Issue(**result["data"]["issueUpdate"]["issue"])

    async def get_issue(self, issue_id):

        result = await self._arun_graphql_query(
            QUERIES["get_issue"],
            variables={
                "id": issue_id,
            },
        )
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return Issue(**result["data"]["issue"])

    async def assign_issue(self, issue_id: str, assignee_id: Optional[str]) -> Issue:
        variables = {
            "id": issue_id,
            "assigneeId": assignee_id,
        }
        result = await self._arun_graphql_query(QUERIES["assign_issue"], variables)
        print(f"Assign issue result: {result}")
        if "errors" in result:
            raise LinearError(result["errors"])
        return Issue(**result["data"]["issueUpdate"]["issue"])

    async def list_users(self) -> List[User]:
        result = await self._arun_graphql_query(QUERIES["list_users"])
        print(f"List users result: {result}")
        if "errors" in result:
            raise LinearError(result["errors"])
        return [User(**user) for user in result["data"]["users"]["nodes"]]

    def list_issue_labels(self) -> List[IssueLabel]:
        result = self._run_graphql_query(QUERIES["list_issue_labels"])
        if "errors" in result:
            raise LinearError(result["errors"])
        return [IssueLabel(**user) for user in result["data"]["issueLabels"]["nodes"]]

    async def list_projects(self) -> List[Project]:
        LINEAR_API_KEY, LINEAR_TEAM_ID = self._get_api_key_and_team_id()
        variables = {
            "teamId": LINEAR_TEAM_ID,
        }
        print("variables:", json.dumps(variables))
        # TODO: if/when we refactor to support multiple teams, we'll need to change this
        result = await self._arun_graphql_query(QUERIES["list_projects_for_team"], variables)
        print(f"List projects result: {result}")
        if "errors" in result:
            raise LinearError(result["errors"])
        return [Project(**project) for project in result["data"]["team"]["projects"]["nodes"]]

    async def create_project(self, input: ProjectInput):
        LINEAR_API_KEY, LINEAR_TEAM_ID = self._get_api_key_and_team_id()

        variables = {
            "teamIds": [LINEAR_TEAM_ID],
            "name": input.name,
            "description": input.description,
            }
        print("variables:", json.dumps(variables))
        result = await self._arun_graphql_query(QUERIES["create_project"], variables)
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return Project(**result["data"]["projectCreate"]["project"])

    async def update_project(self, project_id, project: ProjectInput):
        LINEAR_API_KEY, LINEAR_TEAM_ID = self._get_api_key_and_team_id()
        variables = {
            "id": project_id,
            "teamIds": [LINEAR_TEAM_ID],
        }
        if project.name is not None:
            variables["name"] = project.name
        if project.description is not None:
            variables["description"] = project.description
        result = await self._arun_graphql_query(QUERIES["update_project"], variables)
        print("variables:", json.dumps(variables))
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return Project(**result["data"]["projectUpdate"]["project"])
        
    async def delete_project(self, project_id) -> bool:
        result = await self._arun_graphql_query(
            QUERIES["delete_project"],
            variables={
                "id": project_id,
            },
        )
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return result["data"]["projectDelete"]["success"]

    # project document endpoints
    async def list_documents(self, project_id: str) -> List[Document]:
        result = await self._arun_graphql_query(
            QUERIES["list_documents"],
            variables={
                "projectId": project_id,
            },
        )
        print(f"List documents result: {result}")
        if "errors" in result:
            raise LinearError(result["errors"])
        return [Document(**doc) for doc in result["data"]["project"]["documents"]["nodes"]]

    async def create_document(self, project_id: str, input: DocumentInput):
        variables = {
            "projectId": project_id,
            "title": input.title,
            "content": input.content,
        }
        print("variables:", json.dumps(variables))
        result = await self._arun_graphql_query(QUERIES["create_document"], variables)
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return Document(**result["data"]["documentCreate"]["document"])

    async def update_document(self, document_id: str, input: DocumentInput):
        variables = {
            "id": document_id,
        }
        if input.name is not None:
            variables["name"] = input.name
        if input.content is not None:
            variables["content"] = input.content
        result = await self._arun_graphql_query(QUERIES["update_document"], variables)
        print("variables:", json.dumps(variables))
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return Document(**result["data"]["documentUpdate"]["document"])

    async def delete_document(self, document_id: str) -> bool:
        result = await self._arun_graphql_query(
            QUERIES["delete_document"],
            variables={
                "id": document_id,
            },
        )
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return result["data"]["documentDelete"]["success"]

    async def get_document(self, document_id: str) -> Document:
        result = await self._arun_graphql_query(
            QUERIES["get_document"],
            variables={
                "id": document_id,
            },
        )
        print(result)
        if "errors" in result:
            raise LinearError(result["errors"])
        return Document(**result["data"]["document"])
