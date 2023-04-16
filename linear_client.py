import os
from typing import List, Optional
import requests
import json

from pydantic import BaseModel

from linear_types import Issue, WorkflowState

class ListIssueFilter(BaseModel):
    stateId: Optional[str]

class IssueInput(BaseModel):
    title: str
    description: str
    priority: float
    stateId: Optional[str]
    # teamId: Optional[str]


QUERIES = {
        "get_issue": """
query Issue($id: String!) {
    issue(id: $id) {
        id
        title
        identifier
        priority
        state {
          id
          name
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
        state {
          id
          name
        }
    }
  }
}""",
    "create_issue": """mutation IssueCreate($title: String!, $description: String!, $priority: Int!, $teamId: String!, $stateId: String) {
    issueCreate(input: {title: $title, description: $description, priority: $priority, teamId: $teamId, stateId: $stateId}) {
        issue {
            id
            title
            identifier
            priority
            stateId
            }}}""",
    "delete_issue": """mutation IssueDelete($issueDeleteId: String!) {
  issueDelete(id: $issueDeleteId) {
    success
  }
}""",
    "update_issue": """mutation IssueUpdate($id: String!, $title: String!, $description: String!, $priority: Int!, $teamId: String!, $stateId: String) {
    issueUpdate(id: $id, input: {title: $title, description: $description, priority: $priority, teamId: $teamId, stateId: $stateId}) {
        issue {
            id
            title
            identifier
            priority
            state {
              id
              name
            }
            }}}""",
    "list_workflow_states": """query {
  workflowStates {
    nodes {
      id
      name
    }
  } }""",

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

    def list_issues(self, filter: Optional[ListIssueFilter] = None):
        variables={
            "filter": {
                "team": {
                    "id": {
                        "eq": LINEAR_TEAM_ID,
                    }
                },
            }
        }
        if filter and 'stateId' in filter:
            variables["filter"]["state"] = {
                "id": {
                    "eq": filter['stateId'],
                }
            }
        result = self._run_graphql_query(
            QUERIES["list_issues"],
            variables=variables,
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
        variables={
                   "id": issue_id, 
                   "title": issue.title,
                   "description": issue.description,
                   "priority": issue.priority,
                   "teamId": LINEAR_TEAM_ID,
                   }
        result = self._run_graphql_query(QUERIES["update_issue"], variables)
        print("variables:",json.dumps(variables))
        print(result)
        if 'errors' in result:
            raise Exception(result['errors'])
        return Issue(**result["data"]["issueUpdate"]["issue"])

    def list_workflow_states(self):
        result = self._run_graphql_query(
            QUERIES["list_workflow_states"],
            variables={}
        )
        print(result)
        if "errors" in result:
            raise Exception(result["errors"])
        return [WorkflowState(**workflow_state) for workflow_state in result["data"]["workflowStates"]["nodes"]]


    def get_issue(self, issue_id):

        result = self._run_graphql_query(
            QUERIES["get_issue"],
            variables={
                "id": issue_id,
            },
        )
        print(result)
        if "errors" in result:
            raise Exception(result["errors"])
        return Issue(**result["data"]["issue"])

