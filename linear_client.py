import os
from typing import List
import requests
import json

from pydantic import BaseModel

from linear_types import Issue

class IssueInput(BaseModel):
    title: str
    description: str
    priority: float
    teamId: str


QUERIES = {
        "list_issues": """
query Issues($filter: IssueFilter) {
  issues(filter: $filter) {
    nodes {
        id
        title
        identifier
        priority
    }
  }
}""",
    "create_issue": """mutation IssueCreate($title: String!, $description: String!, $priority: IssuePriority!) {
    issueCreate(input: {title: $title, description: $description, priority: $priority}) {
        issue {
            id
            title
            identifier
            priority
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
        return self.session.post(self.endpoint,
                                 json={
                                     "query": query,
                                     "variables": variables or {},
                                     },
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {LINEAR_API_KEY}',
                                     }
                                 ).json()

    def list_issues(self):
        result = self._run_graphql_query(QUERIES["list_issues"], variables={
            "filter": {
                "team": {
                    "id": {
                        "eq": LINEAR_TEAM_ID,
                        }
                    },
                }
            }
        )
        print(result)
        if 'errors' in result:
            raise Exception(result['errors'])
        return [Issue(**issue) for issue in result["data"]["issues"]["nodes"]]

    def create_issue(self, input: IssueInput):
        # TODO(Can we just pass the whole input as variables?)
        result = self._run_graphql_query(QUERIES["create_issue"], variables={
            "teamId": LINEAR_TEAM_ID,
            "title": input.title,
            "description": input.description,
            "priority": input.priority,
        })
        print(input)
        print(result)
        if 'errors' in result:
            raise Exception(result['errors'])
        return Issue(**result["data"]["issue"])
