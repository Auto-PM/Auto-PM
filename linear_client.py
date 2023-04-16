import os
from typing import List, Optional
import requests
import json

from pydantic import BaseModel, Field

from linear_types import Issue


# class Status(Enum):
#     IN_REVIEW = "7c0bbc28-ffce-45b4-b432-d9223c2330a9"
#     IN_PROGRESS = "f4bf4bfa-7a53-4b9c-8a5f-6efd2167afd4"
#     # TODO = "Todo"
#     # CANCELLED = "Cancelled"
#     # DONE = "Done"
#     # BACKLOG = "Backlog"


from enum import Enum, auto
from typing import Any

status = {
    "in_review": "7c0bbc28-ffce-45b4-b432-d9223c2330a9",
    "in_progress": "f4bf4bfa-7a53-4b9c-8a5f-6efd2167afd4",
    "cancelled": "ab54a373-3661-44f8-9cb8-c464fab63bc6",
    "done": "09e6c51b-8ff9-4c5a-a797-4afd3cae9fa1",
    "backlog": "15645ccf-4883-48fb-9483-d194b9cb19a1",
    "todo": "4781c172-be3b-43fd-9db1-55924c2d46d8",
}


class IssueState(Enum):
    IN_REVIEW = "in_review"
    IN_PROGRESS = "in_progress"

    def state_id(self) -> Any:
        return status[self.name.lower()]


class IssueInput(BaseModel):
    title: str
    description: str
    priority: float
    state: IssueState = Field(
        ...,
        description="Issue state/status. The current status of the issue. (accepted values: 'in_review', 'in_progress', 'todo', 'done', 'backlog', 'cancelled')",
        example=IssueState.IN_REVIEW,
    )


QUERIES = {
    "list_issues": """
query Issues($filter: IssueFilter) {
  issues(filter: $filter) {
    nodes {
        id
        title
        identifier
        priority
        state {
            name
      }
    }
  }
}""",
    "create_issue": """mutation IssueCreate($title: String!, $description: String!, $priority: Int!, $teamId: String!, $stateId: String!) {
    issueCreate(input: {title: $title, description: $description, priority: $priority, teamId: $teamId, stateId: $stateId}) {
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
    "update_issue": """mutation IssueUpdate($id: String!, $title: String!, $description: String!, $priority: Int!, $teamId: String!, $stateId: String!) {
    issueUpdate(id: $id, input: {title: $title, description: $description, priority: $priority, teamId: $teamId, stateId: $stateId}) {
        issue {
            id
            title
            identifier
            priority
            state {
            name
      }
            }}}""",
}

LINEAR_API_KEY = os.environ["LINEAR_API_KEY"]
# TODO: this is a hack, we should get the team id from the API
LINEAR_TEAM_ID = os.environ["LINEAR_TEAM_ID"]


class LinearClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()

    def _run_graphql_query(self, query, variables=None):
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

    def list_issues(self):
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
        # TODO(Can we just pass the whole input as variables?)
        variables = {
            "teamId": LINEAR_TEAM_ID,
            "title": input.title,
            "description": input.description,
            "priority": input.priority,
            "stateId": input.state.state_id(),
        }
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

    def update_issue(self, issue_id, issue):
        variables = {
            "id": issue_id,
            "title": issue.title,
            "description": issue.description,
            "priority": issue.priority,
            "teamId": LINEAR_TEAM_ID,
            "stateId": input.state.state_id(),
        }
        result = self._run_graphql_query(QUERIES["update_issue"], variables)
        print("variables:", json.dumps(variables))
        print(result)
        if "errors" in result:
            raise Exception(result["errors"])
        return Issue(**result["data"]["issueUpdate"]["issue"])
