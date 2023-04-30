"""This file contains all the queries used in the linear_client.py file"""

QUERIES = {
    "get_issue": """
query Issue($id: String!) {
    issue(id: $id) {
        id
        title
        identifier
        description
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
    "create_issue": """mutation IssueCreate(
      $title: String!
      $description: String!
      $priority: Int
      $teamId: String!
      $stateId: String!
      $parentId: String
      $projectId: String
    ) {
      issueCreate(
        input: {
          title: $title
          description: $description
          priority: $priority
          teamId: $teamId
          stateId: $stateId
          parentId: $parentId
          projectId: $projectId
        }
      ) {
        issue {
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
    "delete_issue": """mutation IssueDelete($issueDeleteId: String!) {
  issueDelete(id: $issueDeleteId) {
    success
  }
}""",
    "update_issue": """mutation IssueUpdate(
      $id: String!
      $title: String
      $description: String
      $priority: Int
      $teamId: String!
      $stateId: String
      $labelIds: [String!]
    ) {
      issueUpdate(
        id: $id
        input: {
          title: $title
          description: $description
          priority: $priority
          teamId: $teamId
          stateId: $stateId
          labelIds: $labelIds
        }
      ) {
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
        }
      }
    }""",

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
# list projects_for_team
"list_projects_for_team": """query ListProjects($teamId: String!) {
    team(id: $teamId) {
      projects {
        nodes {
          id
          name
          state
          documents {
            nodes   {
              id
              content
              contentData
            }
          }
        }
      }
    }
}""",

# create project:
"create_project": """
    mutation CreateProject(
      $teamIds: [String!]!
      $name: String!
      $description: String
      $state: String
    ) {
      projectCreate(
        input: {
          teamIds: $teamIds
          name: $name
          description: $description
          state: $state
        }
      ) {
        project {
          id
          name
          description
        }
      }
    }""",

# delete project:
"delete_project": """
    mutation DeleteProject($id: String!) {
        projectDelete(id: $id) {
            success
        }
    }""",
# document queries
"create_document": """
    mutation CreateDocument(
      $projectId: String!
      $title: String!
      $content: String!
      $contentData: JSONObject
    ) {
      documentCreate(
        input: {
          projectId: $projectId
          title: $title
          content: $content
          contentData: $contentData
        }
      ) {
        document {
          id
          title
          content
          contentData
        }
      }
    }""",

"get_document": """
    query Document($id: String!) {
        document(id: $id) {
            id
            title
            content
            contentData
       }
    }""",
}
        
