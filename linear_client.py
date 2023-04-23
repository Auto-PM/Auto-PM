import os
from typing import List, Optional
import requests
import json

from pydantic import BaseModel, Field
from typing import Optional

from linear_types import Issue, User, IssueLabel

from enum import Enum, auto
from typing import Any

import httpx


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
    title: str
    description: str
    priority: float
    state: IssueState = Field(
        ...,
        description="Issue state/status. The current status of the issue. If a user asks to mark an issue a certain status you should not mention it anywhere in the title or description but instead just mark it here in 'state'. (accepted values: 'in_review', 'in_progress', 'todo', 'done', 'backlog', 'cancelled')",
        example=IssueState.IN_REVIEW,
    )
    label_ids: Optional[List[str]] = None
    parent_id: Optional[str] = None


class AssignIssueInput(BaseModel):
    issue_id: str
    assignee_id: str


class IssueModificationInput(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[float] = None
    state: Optional[IssueState] = Field(
        None,
        description="Issue state/status. The current status of the issue. (accepted values: 'in_review', 'in_progress', 'todo', 'done', 'backlog', 'cancelled')",
        example=IssueState.IN_REVIEW,
    )
    label_ids: Optional[List[str]] = None


QUERIES = {
    "get_issue": """
query Issue($id: String!) {
    issue(id: $id) {
        id
        title
        identifier
        priority
        parent {
          id
           identifier
        }
        assignee {
          id
          name
        }
        state {
          id
          name
        }
        labels {
          nodes {
            id
            name
          }
        }
        }}""",
    "list_issues": """
query Issues($filter: IssueFilter) {
  issues(filter: $filter) {
    nodes {
        id
        title
        identifier
        priority
        parent {
          id
        }
        state {
            name
        }
        assignee {
          id
          name
        }
        labels {
          nodes {
            id
            name
          }
        }
    }
  }
}""",
    "create_issue": """mutation IssueCreate($title: String!, $description: String!, $priority: Int!, $teamId: String!, $stateId: String!, $parentId: String) {
    issueCreate(input: {title: $title, description: $description, priority: $priority, teamId: $teamId, stateId: $stateId, parentId: $parentId}) {
        issue {
            id
            title
            identifier
            priority
            state {
              name
            }
            }}}""",
    "delete_issue": """mutation IssueDelete($issueDeleteId: String!) {
  issueDelete(id: $issueDeleteId) {
    success
  }
}""",
    "update_issue": """mutation IssueUpdate($id: String!, $title: String, $description: String, $priority: Int, $teamId: String!, $stateId: String, $labelIds: [String!]) {
    issueUpdate(id: $id, input: {title: $title, description: $description, priority: $priority, teamId: $teamId, stateId: $stateId, labelIds: $labelIds}) {
        issue {
            id
            title
            identifier
            priority
            state {
              id
              name
            }
            labels {
              nodes {
                id
                name
              }
            }
            }}}""",
    "assign_issue": """
mutation IssueUpdateAssignee($id: String!, $assigneeId: String) {
  issueUpdate(id: $id, input: {assigneeId: $assigneeId}) {
    issue {
      id
      title
      identifier
      priority
      state {
        name
      }
      assignee {
        id
        name
      }
    }
  }
}
""",
    "list_users": """
query Users {
  users {
    nodes {
      id
      name
      email
    }
  }
}
""",
    "list_issue_labels": """
query IssueLabels {
  issueLabels {
    nodes {
      id
      name
    }
  }
}
""",
}

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

    def list_issues(self):
        LINEAR_API_KEY, LINEAR_TEAM_ID = self._get_api_key_and_team_id()
        result = self._run_graphql_query(
            QUERIES["list_issues"],
            variables={
                "filter": {
                    "team": {
                        "id": {
                            "eq": LINEAR_TEAM_ID,
                        }
                    },
                }
            },
        )
        print(result)
        if "errors" in result:
            raise Exception(result["errors"])
        return [Issue(**issue) for issue in result["data"]["issues"]["nodes"]]

    def create_issue(self, input: IssueInput):
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
        result = self._run_graphql_query(QUERIES["create_issue"], variables)
        print("variables:", json.dumps(variables))
        print(result)
        if "errors" in result:
            raise Exception(result["errors"])
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
            raise Exception(result["errors"])
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
            raise Exception(result["errors"])
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
            raise Exception(result["errors"])
        return Issue(**result["data"]["issue"])

    async def assign_issue(self, issue_id: str, assignee_id: Optional[str]) -> Issue:
        variables = {
            "id": issue_id,
            "assigneeId": assignee_id,
        }
        result = await self._arun_graphql_query(QUERIES["assign_issue"], variables)
        print(f"Assign issue result: {result}")
        if "errors" in result:
            raise Exception(result["errors"])
        return Issue(**result["data"]["issueUpdate"]["issue"])

    def list_users(self) -> List[User]:
        result = self._run_graphql_query(QUERIES["list_users"])
        print(f"List users result: {result}")
        if "errors" in result:
            raise Exception(result["errors"])
        return [User(**user) for user in result["data"]["users"]["nodes"]]

    def list_issue_labels(self) -> List[IssueLabel]:
        result = self._run_graphql_query(QUERIES["list_issue_labels"])
        if "errors" in result:
            raise Exception(result["errors"])
        return [IssueLabel(**user) for user in result["data"]["issueLabels"]["nodes"]]
