"""This file contains all the queries used in the linear_client.py file"""

QUERIES = {
    "get_teams": """
      query Teams {
          teams {
            nodes {
              id
              name
            }
          }
        }
        """,
    "get_workflow_states": """
        query Teams($filter: TeamFilter) {
  teams(filter: $filter) {
    nodes {
      states {
        nodes {
          name
          id
        }
      }
    }
  }
}
""",
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
        projectMilestone {
          id
          name
        }
        comments {
          nodes {
            id
            body
            user {
              name
              email
              isMe
            }
          }
        }
        children {
          nodes {
            id
            title
            state {
              id
              name
            }
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
        projectMilestone {
          id
          name
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
      $projectMilestoneId: String
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
          projectMilestoneId: $projectMilestoneId
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
          projectMilestone {
            id
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
      $projectId: String 
      $projectMilestoneId: String
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
          projectId: $projectId
          projectMilestoneId: $projectMilestoneId
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
          projectMilestone {
            id
            name
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
    # get project:
    "get_project": """
    query Project($id: String!) {
        project(id: $id) {
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
    """,
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
    # update project:
    "update_project": """
    mutation UpdateProject(
        $id: String!
        $name: String
        $description: String
        $state: String
    ) {
        projectUpdate(
            id: $id
            input: {
                name: $name
                description: $description
                state: $state
            }
        ) {
            project {
                id
                name
                description
                state
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
    # update document:
    "update_document": """
    mutation UpdateDocument(
        $id: String!
        $title: String
        $content: String
        $contentData: JSONObject
    ) {
        documentUpdate(
            id: $id
            input: {
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
    # list documents:
    "list_documents": """
    query ListDocuments($projectId: String!) {
        project(id: $projectId) {
            documents {
                nodes {
                    
                    id
                    title
                    content
                    contentData
                }
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
    "list_milestones": """
    query ListProjectMilestones($projectId: String!) {
      project(id: $projectId) {
        projectMilestones {
          nodes {
            id
            name
            description
            targetDate
          }
        }
      }
    }
    """,
    "create_milestone": """
    mutation CreateProjectMilestone(
      $projectId: String!
      $name: String!
      $description: String
      $targetDate: TimelessDate
      $sortOrder: Float
    ) {
      projectMilestoneCreate(
        input: {
          projectId: $projectId
          name: $name
          description: $description
          targetDate: $targetDate
          sortOrder: $sortOrder
        }
      ) {
        projectMilestone {
          id
          name
          description
          targetDate
          sortOrder
        }
      }
    }

""",
    "delete_milestone": """
    mutation DeleteProjectMilestone($id: String!) {
        projectMilestoneDelete(id: $id) {
            success
        }
    }
""",
    "update_milestone": """
    mutation UpdateProjectMilestone(
      $id: String!
      $name: String
      $description: String
      $targetDate: TimelessDate
      $sortOrder: Float
    ) {
      projectMilestoneUpdate(
        id: $id
        input: {
          name: $name
          description: $description
          targetDate: $targetDate
          sortOrder: $sortOrder
        }
      ) {
        projectMilestone {
          id
          name
          description
          targetDate
          sortOrder
        }
      }
    }
""",
    # create comment
    "create_comment": """
    mutation CreateComment($issueId: String!, $body: String!, $parentId: String) {
      commentCreate(
        input: { issueId: $issueId, body: $body, parentId: $parentId }
      ) {
        comment {
          id
          body
        }
      }
    }
""",
                        
"create_attachment": """mutation CreateAttachment(
        $issueId: String!
        $commentBody: String
        $title: String!
        $subtitle: String
        $metadata: JSONObject
        $url: String!
    ) {
    attachmentCreate(input: {
        issueId: $issueId
        commentBody: $commentBody
        title: $title
        subtitle: $subtitle
        metadata: $metadata
        url: $url
    }) {
        attachment {
        id
        title
        subtitle
        metadata
        source
        sourceType
        }
        }}
""",

}

