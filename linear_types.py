from __future__ import annotations

from typing import Any, Optional, List
from pydantic import BaseModel

class PageInfo(BaseModel):
    end_cursor: Optional[str]
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]

class IssueLabelConnection(BaseModel):
    #edges: List["IssueLabelEdge"]
    nodes: List["IssueLabel"]
    #page_info: "PageInfo"


class IssueLabel(BaseModel):
    # archived_at: Any
    # children: "IssueLabelConnection"
    # color: str
    # created_at: Any
    #creator: Optional["User"]
    #description: Optional[str]
    id: Optional[str]
    #issues: "IssueConnection"
    name: str
    #parent: Optional["IssueLabel"]
    #team: Optional["Team"]
    # updated_at: Any

IssueLabelConnection.update_forward_refs()  

class IssueConnection(BaseModel):
    #edges: list["IssueEdge"]
    nodes: Optional[List[Optional['Issue']]]
    #page_info: PageInfo


class IssueEdge(BaseModel):
    cursor: str
    node: Issue


class Issue(BaseModel):
    archived_at: Any
    assignee: Optional[AssigneeUser]
    attachments: Optional['AttachmentConnection']
    # auto_archived_at: Any
    # auto_closed_at: Any
    # branch_name: str
    # canceled_at: Any
    children: Optional['IssueConnection']
    # children: Optional[list["Issue"]]
    comments: Optional['CommentConnection']
    # completed_at: Any
    # created_at: Any
    # creator: Optional['User']
    # customer_ticket_count: int
    # cycle: Optional['Cycle']
    description: Optional[str]
    # description_data: Any
    # due_date: Any
    # estimate: Optional[float]
    # external_user_creator: Optional['ExternalUser']
    # history: 'IssueHistoryConnection'
    id: str
    identifier: Optional[str]
    # inverse_relations: 'IssueRelationConnection'
    labels: Optional[IssueLabelConnection]
    # number: float
    parent: Optional["Issue"]
    # previous_identifiers: List[str]
    priority: Optional[float]
    # priority_label: str
    # project: Optional['Project']
    project_milestone: Optional['ProjectMilestone']
    # relations: 'IssueRelationConnection'
    # sla_breaches_at: Any
    # sla_started_at: Any
    # snoozed_by: Optional['User']
    # snoozed_until_at: Any
    # sort_order: float
    # started_at: Any
    # started_triage_at: Any
    state: Optional['WorkflowState']
    # sub_issue_sort_order: Optional[float]
    # subscribers: 'UserConnection'
    # team: 'Team'
    title: Optional[str]
    # trashed: Optional[bool]
    # triaged_at: Any
    # updated_at: Any
    # url: str


class IssueBatchPayload(BaseModel):
    issues: List["Issue"]
    last_sync_id: float
    success: bool


class IssueCollectionFilter(BaseModel):
    and_: Optional[List["IssueCollectionFilter"]]
    assignee: Optional["NullableUserFilter"]
    attachments: Optional["AttachmentCollectionFilter"]
    auto_archived_at: Optional["NullableDateComparator"]
    auto_closed_at: Optional["NullableDateComparator"]
    canceled_at: Optional["NullableDateComparator"]
    children: Optional["IssueCollectionFilter"]
    comments: Optional["CommentCollectionFilter"]
    completed_at: Optional["NullableDateComparator"]
    created_at: Optional["DateComparator"]
    creator: Optional["NullableUserFilter"]
    cycle: Optional["NullableCycleFilter"]
    description: Optional["NullableStringComparator"]
    due_date: Optional["NullableTimelessDateComparator"]
    estimate: Optional["EstimateComparator"]
    every: Optional["IssueFilter"]
    has_blocked_by_relations: Optional["RelationExistsComparator"]
    has_blocking_relations: Optional["RelationExistsComparator"]
    has_duplicate_relations: Optional["RelationExistsComparator"]
    has_related_relations: Optional["RelationExistsComparator"]
    id: Optional["IDComparator"]
    labels: Optional["IssueLabelCollectionFilter"]
    length: Optional["NumberComparator"]
    number: Optional["NumberComparator"]
    or_: Optional[List["IssueCollectionFilter"]]
    parent: Optional["NullableIssueFilter"]
    priority: Optional["NullableNumberComparator"]
    project: Optional["NullableProjectFilter"]
    project_milestone: Optional["NullableProjectMilestoneFilter"]
    searchable_content: Optional["ContentComparator"]
    sla_status: Optional["SlaStatusComparator"]
    snoozed_by: Optional["NullableUserFilter"]
    snoozed_until_at: Optional["NullableDateComparator"]
    some: Optional["IssueFilter"]
    started_at: Optional["NullableDateComparator"]
    state: Optional["WorkflowStateFilter"]
    subscribers: Optional["UserCollectionFilter"]
    team: Optional["TeamFilter"]
    title: Optional["StringComparator"]
    triaged_at: Optional["NullableDateComparator"]
    updated_at: Optional["DateComparator"]


class IssueCreateInput(BaseModel):
    assignee_id: Optional[str]
    board_order: Optional[float]
    create_as_user: Optional[str]
    created_at: Any
    cycle_id: Optional[str]
    description: Optional[str]
    description_data: Any
    display_icon_url: Optional[str]
    due_date: Any
    estimate: Optional[int]
    id: Optional[str]
    label_ids: Optional[List[str]]
    parent_id: Optional[str]
    priority: Optional[int]
    project_id: Optional[str]
    project_milestone_id: Optional[str]
    reference_comment_id: Optional[str]
    sla_breaches_at: Any
    sort_order: Optional[float]
    state_id: Optional[str]
    sub_issue_sort_order: Optional[float]
    subscriber_ids: Optional[List[str]]
    team_id: str
    title: str


class User(BaseModel):
    # active: bool
    # admin: bool
    # archived_at: Any
    # assigned_issues: 'IssueConnection'
    # avatar_url: Optional[str]
    # calendar_hash: Optional[str]
    # created_at: Any
    # created_issue_count: int
    # created_issues: 'IssueConnection'
    # description: Optional[str]
    # disable_reason: Optional[str]
    # display_name: str
    email: str
    # guest: bool
    id: str
    # invite_hash: str
    is_me: Optional[bool]
    # last_seen: Any
    name: str
    # organization: 'Organization'
    # status_emoji: Optional[str]
    # status_label: Optional[str]
    # status_until_at: Any
    # team_memberships: 'TeamMembershipConnection'
    # teams: 'TeamConnection'
    # timezone: Optional[str]
    # updated_at: Any
    # url: str


class AssigneeUser(BaseModel):
    # active: bool
    # admin: bool
    # archived_at: Any
    # assigned_issues: 'IssueConnection'
    # avatar_url: Optional[str]
    # calendar_hash: Optional[str]
    # created_at: Any
    # created_issue_count: int
    # created_issues: 'IssueConnection'
    # description: Optional[str]
    # disable_reason: Optional[str]
    # display_name: str
    email: Optional[str]
    # guest: bool
    id: Optional[str]
    # invite_hash: str
    is_me: Optional[bool]
    # last_seen: Any
    name: Optional[str]
    # organization: 'Organization'
    # status_emoji: Optional[str]
    # status_label: Optional[str]
    # status_until_at: Any
    # team_memberships: 'TeamMembershipConnection'
    # teams: 'TeamConnection'
    # timezone: Optional[str]
    # updated_at: Any
    # url: str


class WorkflowState(BaseModel):
    # archived_at: Any
    # color: str
    # created_at: Any
    description: Optional[str]
    id: Optional[str]
    # issues: "IssueConnection"
    name: Optional[str]
    # position: float
    # team: "Team"
    # _type: str
    # updated_at: Any


class Project(BaseModel):
    # archived_at: Optional[Any]
    # auto_archived_at: Optional[Any]
    # canceled_at: Optional[Any]
    # color: Optional[str]
    # completed_at: Optional[Any]
    # # completed_issue_count_history: List[float]
    # # completed_scope_history: List[float]
    # # converted_from_issue: Optional["Issue"]
    # # created_at: Any
    # creator: Optional["User"]
    # description: Optional[str]
    # documents: Optional["DocumentConnection"]
    # icon: Optional[str]
    id: Optional[str]
    in_progress_scope_history: Optional[List[float]]
    #integrations_settings: Optional["IntegrationsSettings"]
    issue_count_history: Optional[List[float]]
    # issues: Optional["IssueConnection"]
    # lead: Optional[Optional["User"]]
    # links: "ProjectLinkConnection"
    # members: "UserConnection"
    name: Optional[str]
    progress: Optional[float]
    project_milestones: Optional["ProjectMilestoneConnection"]
    # project_update_reminders_paused_until_at: Any
    # project_updates: "ProjectUpdateConnection"
    # scope: float
    # scope_history: List[float]
    # slack_issue_comments: bool
    # slack_issue_statuses: bool
    # slack_new_issue: bool
    slug_id: Optional[str]
    # sort_order: float
    # start_date: Any
    # started_at: Any
    state: Optional[str]
    # target_date: Any
    # teams: "TeamConnection"
    updated_at: Optional[Any]
    url: Optional[str]


class Document(BaseModel):
    archived_at: Optional[Any]
    color: Optional[str]
    content: Optional[str]
    content_data: Optional[Any]
    created_at: Optional[Any]
    creator: Optional["User"]
    icon: Optional[str]
    id: Optional[str]
    project: Optional["Project"]
    slug_id: Optional[str]
    title: Optional[str]
    updated_at: Optional[Any]
    updated_by: Optional["User"]


class DocumentConnection(BaseModel):
    # edges: Optional[List["DocumentEdge"]]
    nodes: Optional[List["Document"]]
    page_info: Optional["PageInfo"]


class DocumentCreateInput(BaseModel):
    color: Optional[str]
    content: Optional[str]
    content_data: Any
    icon: Optional[str]
    id: Optional[str]
    project_id: st
    title: str


class DocumentEdge(BaseModel):
    cursor: Optional[str]
    node: Optional["Document"]


class DocumentPayload(BaseModel):
    document: "Document"
    last_sync_id: float
    success: bool


class DocumentUpdateInput(BaseModel):
    color: Optional[str]
    content: Optional[str]
    content_data: Any
    icon: Optional[str]
    project_id: Optional[str]
    title: Optional[str]


class ProjectMilestone(BaseModel):
    # archived_at: Any
    # created_at: Any
    id: str
    name: str
    description: Optional[str]
    project: Optional["Project"]
    sort_order: Optional[float]
    target_date: Optional[Any]
    updated_at: Optional[Any]


class ProjectMilestoneConnection(BaseModel):
    nodes: List["ProjectMilestone"]
    page_info: "PageInfo"


class ProjectMilestoneInput(BaseModel):
    description: Optional[str]
    id: Optional[str]
    name: str
    # project_id: str
    sort_order: Optional[float]
    target_date: Any


class Comment(BaseModel):
    archived_at: Optional[Any]
    body: Optional[str]
    body_data: Optional[str]
    #children: Optional["CommentConnection"]
    created_at: Optional[Any]
    edited_at: Optional[Any]
    #external_user: Optional["ExternalUser"]
    id: str
    issue: Optional["Issue"]
    #parent: Optional["Comment"]
    reaction_data: Optional[Any]
    updated_at: Optional[Any]
    url: Optional[str]
    #user: Optional["User"]


class CommentConnection(BaseModel):
    # edges: List["CommentEdge"]
    nodes: List[Optional["Comment"]]
    # page_info: "PageInfo"


class ExternalUser(BaseModel):
    archived_at: Any
    avatar_url: Optional[str]
    created_at: Any
    display_name: str
    email: str
    id: str
    last_seen: Any
    name: str
    # organization: "Organization"
    updated_at: Any


class CommentCreateInput(BaseModel):
    body: Optional[str]
    body_data: Optional[Any]
    create_as_user: Optional[str]
    created_at: Optional[Any]
    display_icon_url: Optional[str]
    do_not_subscribe_to_issue: Optional[bool]
    id: Optional[str]
    issue_id: str
    parent_id: Optional[str]


class Attachment(BaseModel):
    archived_at: Optional[Any]
    created_at: Optional[Any]
    creator: Optional['User']
    group_by_source: Optional[bool]
    id: Optional[str]
    issue: Optional['Issue']
    metadata: Optional[dict]
    source: Optional[Any]
    source_type: Optional[str]
    subtitle: Optional[str]
    title: Optional[str]
    updated_at: Optional[Any]
    url: Optional[str]


class AttachmentConnection(BaseModel):
    #edges: List["AttachmentEdge"]
    nodes: List["Attachment"]
    #page_info: "PageInfo"


class AttachmentCreateInput(BaseModel):
    comment_body: Optional[str]
    comment_body_data: Optional[Any]
    create_as_user: Optional[str]
    group_by_source: Optional[bool]
    icon_url: Optional[str]
    id: Optional[str]
    issue_id: str
    metadata: Optional[Any]
    subtitle: Optional[str]
    title: Optional[str]
    url: Optional[str]


# IssueEdge.update_forward_refs()
Issue.update_forward_refs()
Project.update_forward_refs()
Document.update_forward_refs()
IssueConnection.update_forward_refs()
