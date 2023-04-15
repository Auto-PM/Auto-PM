import os
from typing import List
import requests

from linear_types import Issue

QUERIES = {
    "list_issues": """query { issues { nodes {
    id
    title
    identifier
    priority
    priorityLabel
    } } }"""
}

LINEAR_API_KEY = os.environ["LINEAR_API_KEY"]

class LinearClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()

    def _run_graphql_query(self, query):
        return self.session.post(self.endpoint,
                                 json={"query": query},
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {LINEAR_API_KEY}',
                                     }
                                 ).json()

    def list_issues(self):
        result = self._run_graphql_query(QUERIES["list_issues"])
        print(result)
        if 'errors' in result:
            raise Exception(result['errors'])
        return [Issue(**issue) for issue in result["data"]["issues"]["nodes"]]
