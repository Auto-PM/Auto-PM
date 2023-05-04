from __future__ import annotations

from enum import Enum
from typing import Any, Optional, List
from pydantic import BaseModel


from linear_types import PageInfo, ProjectMilestone, Comment, ExternalUser

class AirbyteConfigurationInput(BaseModel):
    api_key: str


class Node(BaseModel):
    id: str


class ApiKey(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    label: str
    updated_at: Any


class ApiKeyConnection(BaseModel):
    edges: List["ApiKeyEdge"]
    nodes: List["ApiKey"]
    page_info: "PageInfo"


class ApiKeyCreateInput(BaseModel):
    id: Optional[str]
    key: str
    label: str


class ApiKeyEdge(BaseModel):
    cursor: str
    node: "ApiKey"


class ApiKeyPayload(BaseModel):
    api_key: "ApiKey"
    last_sync_id: float
    success: bool


class Application(BaseModel):
    client_id: str
    description: Optional[str]
    developer: str
    developer_url: str
    id: str
    image_url: Optional[str]
    name: str


class ArchivePayload(BaseModel):
    last_sync_id: float
    success: bool


class AttachmentCollectionFilter(BaseModel):
    and_: Optional[List["AttachmentCollectionFilter"]]
    created_at: Optional["DateComparator"]
    creator: Optional["NullableUserFilter"]
    every: Optional["AttachmentFilter"]
    id: Optional["IDComparator"]
    length: Optional["NumberComparator"]
    or_: Optional[List["AttachmentCollectionFilter"]]
    some: Optional["AttachmentFilter"]
    source_type: Optional["SourceTypeComparator"]
    subtitle: Optional["NullableStringComparator"]
    title: Optional["StringComparator"]
    updated_at: Optional["DateComparator"]
    url: Optional["StringComparator"]


class AttachmentEdge(BaseModel):
    cursor: str
    node: "Attachment"


class AttachmentFilter(BaseModel):
    and_: Optional[List["AttachmentFilter"]]
    created_at: Optional["DateComparator"]
    creator: Optional["NullableUserFilter"]
    id: Optional["IDComparator"]
    or_: Optional[List["AttachmentFilter"]]
    source_type: Optional["SourceTypeComparator"]
    subtitle: Optional["NullableStringComparator"]
    title: Optional["StringComparator"]
    updated_at: Optional["DateComparator"]
    url: Optional["StringComparator"]


class AttachmentPayload(BaseModel):
    attachment: "Attachment"
    last_sync_id: float
    success: bool


class AttachmentUpdateInput(BaseModel):
    icon_url: Optional[str]
    metadata: Any
    subtitle: Optional[str]
    title: str


class AuditEntry(BaseModel):
    actor: Optional["User"]
    actor_id: Optional[str]
    archived_at: Any
    country_code: Optional[str]
    created_at: Any
    id: str
    ip: Optional[str]
    metadata: Any
    organization: Optional["Organization"]
    request_information: Any
    type: str
    updated_at: Any


class AuditEntryConnection(BaseModel):
    edges: List["AuditEntryEdge"]
    nodes: List["AuditEntry"]
    page_info: "PageInfo"


class AuditEntryEdge(BaseModel):
    cursor: str
    node: "AuditEntry"


class AuditEntryFilter(BaseModel):
    actor: Optional["NullableUserFilter"]
    country_code: Optional["StringComparator"]
    created_at: Optional["DateComparator"]
    id: Optional["IDComparator"]
    ip: Optional["StringComparator"]
    type: Optional["StringComparator"]
    updated_at: Optional["DateComparator"]


class AuditEntryType(BaseModel):
    description: str
    type: str


class AuthMembership(BaseModel):
    created_at: Any
    user_id: str


class AuthResolverResponse(BaseModel):
    allow_domain_access: Optional[bool]
    available_organizations: Optional[List["Organization"]]
    email: Optional[str]
    id: str
    last_used_organization_id: Optional[str]
    token: Optional[str]
    users: List["User"]


class AuthorizedApplication(BaseModel):
    app_id: str
    client_id: str
    image_url: Optional[str]
    name: str
    scope: List[str]
    webhooks_enabled: bool


class CommentCollectionFilter(BaseModel):
    and_: Optional[List["CommentCollectionFilter"]]
    body: Optional["StringComparator"]
    created_at: Optional["DateComparator"]
    every: Optional["CommentFilter"]
    id: Optional["IDComparator"]
    issue: Optional["IssueFilter"]
    length: Optional["NumberComparator"]
    or_: Optional[List["CommentCollectionFilter"]]
    some: Optional["CommentFilter"]
    updated_at: Optional["DateComparator"]
    user: Optional["UserFilter"]


class CommentEdge(BaseModel):
    cursor: str
    node: "Comment"


class CommentFilter(BaseModel):
    and_: Optional[List["CommentFilter"]]
    body: Optional["StringComparator"]
    created_at: Optional["DateComparator"]
    id: Optional["IDComparator"]
    issue: Optional["IssueFilter"]
    or_: Optional[List["CommentFilter"]]
    updated_at: Optional["DateComparator"]
    user: Optional["UserFilter"]


class CommentPayload(BaseModel):
    comment: "Comment"
    last_sync_id: float
    success: bool


class CommentUpdateInput(BaseModel):
    body: Optional[str]
    body_data: Any


class ContactCreateInput(BaseModel):
    browser: Optional[str]
    client_version: Optional[str]
    device: Optional[str]
    disappointment_rating: Optional[int]
    message: str
    operating_system: Optional[str]
    type: str


class ContactPayload(BaseModel):
    success: bool


class ContactSalesCreateInput(BaseModel):
    email: str
    message: Optional[str]
    name: str


class CreateCsvExportReportPayload(BaseModel):
    success: bool


class CreateOrJoinOrganizationResponse(BaseModel):
    organization: "Organization"
    user: "User"


class CreateOrganizationInput(BaseModel):
    domain_access: Optional[bool]
    name: str
    timezone: Optional[str]
    url_key: str
    utm: Optional[str]


class CustomView(BaseModel):
    archived_at: Any
    color: Optional[str]
    created_at: Any
    creator: "User"
    description: Optional[str]
    filter_data: Any
    icon: Optional[str]
    id: str
    name: str
    organization: "Organization"
    project_filter_data: Any
    shared: bool
    team: Optional["Team"]
    updated_at: Any


class CustomViewConnection(BaseModel):
    edges: List["CustomViewEdge"]
    nodes: List["CustomView"]
    page_info: "PageInfo"


class CustomViewCreateInput(BaseModel):
    color: Optional[str]
    description: Optional[str]
    filter_data: Any
    filters: Any
    icon: Optional[str]
    id: Optional[str]
    name: str
    project_filter_data: Any
    shared: Optional[bool]
    team_id: Optional[str]


class CustomViewEdge(BaseModel):
    cursor: str
    node: "CustomView"


class CustomViewPayload(BaseModel):
    custom_view: "CustomView"
    last_sync_id: float
    success: bool


class CustomViewSuggestionPayload(BaseModel):
    suggested_description: Optional[str]
    suggested_icon: Optional[str]
    suggested_name: Optional[str]


class CustomViewUpdateInput(BaseModel):
    color: Optional[str]
    description: Optional[str]
    filter_data: Any
    filters: Any
    icon: Optional[str]
    name: Optional[str]
    project_filter_data: Any
    shared: Optional[bool]
    team_id: Optional[str]


class Cycle(BaseModel):
    archived_at: Any
    auto_archived_at: Any
    completed_at: Any
    completed_issue_count_history: List[float]
    completed_scope_history: List[float]
    created_at: Any
    description: Optional[str]
    ends_at: Any
    id: str
    in_progress_scope_history: List[float]
    issue_count_history: List[float]
    issues: "IssueConnection"
    name: Optional[str]
    number: float
    progress: float
    scope_history: List[float]
    starts_at: Any
    team: "Team"
    uncompleted_issues_upon_close: "IssueConnection"
    updated_at: Any


class CycleConnection(BaseModel):
    edges: List["CycleEdge"]
    nodes: List["Cycle"]
    page_info: "PageInfo"


class CycleCreateInput(BaseModel):
    completed_at: Any
    description: Optional[str]
    ends_at: Any
    id: Optional[str]
    name: Optional[str]
    starts_at: Any
    team_id: str


class CycleEdge(BaseModel):
    cursor: str
    node: "Cycle"


class CycleFilter(BaseModel):
    and_: Optional[List["CycleFilter"]]
    completed_at: Optional["DateComparator"]
    created_at: Optional["DateComparator"]
    ends_at: Optional["DateComparator"]
    id: Optional["IDComparator"]
    is_active: Optional["BooleanComparator"]
    is_future: Optional["BooleanComparator"]
    is_next: Optional["BooleanComparator"]
    is_past: Optional["BooleanComparator"]
    is_previous: Optional["BooleanComparator"]
    issues: Optional["IssueCollectionFilter"]
    name: Optional["StringComparator"]
    number: Optional["NumberComparator"]
    or_: Optional[List["CycleFilter"]]
    starts_at: Optional["DateComparator"]
    team: Optional["TeamFilter"]
    updated_at: Optional["DateComparator"]


class CyclePayload(BaseModel):
    cycle: Optional["Cycle"]
    last_sync_id: float
    success: bool


class CycleUpdateInput(BaseModel):
    completed_at: Any
    description: Optional[str]
    ends_at: Any
    name: Optional[str]
    starts_at: Any


class Day(str, Enum):
    Friday = "Friday"
    Monday = "Monday"
    Saturday = "Saturday"
    Sunday = "Sunday"
    Thursday = "Thursday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"


class DeleteOrganizationInput(BaseModel):
    deletion_code: str


class EmailSubscribeInput(BaseModel):
    email: str


class EmailSubscribePayload(BaseModel):
    success: bool


class EmailUnsubscribeInput(BaseModel):
    token: str
    type: str
    user_id: str


class EmailUnsubscribePayload(BaseModel):
    success: bool


class EmailUserAccountAuthChallengeInput(BaseModel):
    client_auth_code: Optional[str]
    email: str
    is_desktop: Optional[bool]
    signup_code: Optional[str]


class EmailUserAccountAuthChallengeResponse(BaseModel):
    auth_type: str
    success: bool


class Emoji(BaseModel):
    archived_at: Any
    created_at: Any
    creator: "User"
    id: str
    name: str
    organization: "Organization"
    source: str
    updated_at: Any
    url: str


class EmojiConnection(BaseModel):
    edges: List["EmojiEdge"]
    nodes: List["Emoji"]
    page_info: "PageInfo"


class EmojiCreateInput(BaseModel):
    id: Optional[str]
    name: str
    url: str


class EmojiEdge(BaseModel):
    cursor: str
    node: "Emoji"


class EmojiPayload(BaseModel):
    emoji: "Emoji"
    last_sync_id: float
    success: bool


class EventCreateInput(BaseModel):
    category: str
    data: Any
    subject: str
    target_id: Optional[str]
    value: Optional[float]


class EventPayload(BaseModel):
    success: bool


class ExternalUserConnection(BaseModel):
    edges: List["ExternalUserEdge"]
    nodes: List["ExternalUser"]
    page_info: "PageInfo"


class ExternalUserEdge(BaseModel):
    cursor: str
    node: "ExternalUser"


class Favorite(BaseModel):
    archived_at: Any
    children: "FavoriteConnection"
    created_at: Any
    custom_view: Optional["CustomView"]
    cycle: Optional["Cycle"]
    document: Optional["Document"]
    folder_name: Optional[str]
    id: str
    issue: Optional["Issue"]
    label: Optional["IssueLabel"]
    parent: Optional["Favorite"]
    predefined_view_team: Optional["Team"]
    predefined_view_type: Optional[str]
    project: Optional["Project"]
    project_team: Optional["Team"]
    roadmap: Optional["Roadmap"]
    sort_order: float
    type: str
    updated_at: Any
    user: "User"


class FavoriteConnection(BaseModel):
    edges: List["FavoriteEdge"]
    nodes: List["Favorite"]
    page_info: "PageInfo"


class FavoriteCreateInput(BaseModel):
    custom_view_id: Optional[str]
    cycle_id: Optional[str]
    document_id: Optional[str]
    folder_name: Optional[str]
    id: Optional[str]
    issue_id: Optional[str]
    label_id: Optional[str]
    parent_id: Optional[str]
    predefined_view_team_id: Optional[str]
    predefined_view_type: Optional[str]
    project_id: Optional[str]
    project_team_id: Optional[str]
    roadmap_id: Optional[str]
    sort_order: Optional[float]


class FavoriteEdge(BaseModel):
    cursor: str
    node: "Favorite"


class FavoritePayload(BaseModel):
    favorite: "Favorite"
    last_sync_id: float
    success: bool


class FavoriteUpdateInput(BaseModel):
    folder_name: Optional[str]
    parent_id: Optional[str]
    sort_order: Optional[float]


class FigmaEmbed(BaseModel):
    last_modified: Any
    name: str
    node_name: Optional[str]
    url: Optional[str]


class FigmaEmbedPayload(BaseModel):
    figma_embed: Optional["FigmaEmbed"]
    success: bool


class FrontAttachmentPayload(BaseModel):
    last_sync_id: float
    success: bool


class FrontSettings(BaseModel):
    automate_ticket_reopening_on_cancellation: Optional[bool]
    automate_ticket_reopening_on_comment: Optional[bool]
    automate_ticket_reopening_on_completion: Optional[bool]
    send_note_on_comment: Optional[bool]
    send_note_on_status_change: Optional[bool]


class FrontSettingsInput(BaseModel):
    automate_ticket_reopening_on_cancellation: Optional[bool]
    automate_ticket_reopening_on_comment: Optional[bool]
    automate_ticket_reopening_on_completion: Optional[bool]
    send_note_on_comment: Optional[bool]
    send_note_on_status_change: Optional[bool]


class GitHubCommitIntegrationPayload(BaseModel):
    integration: Optional["Integration"]
    last_sync_id: float
    success: bool
    webhook_secret: str


class GitHubSettings(BaseModel):
    org_avatar_url: str
    org_login: str


class GitHubSettingsInput(BaseModel):
    org_avatar_url: str
    org_login: str


class GithubOAuthTokenPayload(BaseModel):
    organizations: Optional[List["GithubOrg"]]
    token: Optional[str]


class GithubOrg(BaseModel):
    id: str
    is_personal: Optional[bool]
    login: str
    name: str
    repositories: List["GithubRepo"]


class GithubRepo(BaseModel):
    id: str
    name: str


class GoogleSheetsSettings(BaseModel):
    sheet_id: float
    spreadsheet_id: str
    spreadsheet_url: str
    updated_issues_at: Any


class GoogleSheetsSettingsInput(BaseModel):
    sheet_id: float
    spreadsheet_id: str
    spreadsheet_url: str
    updated_issues_at: Any


class GoogleUserAccountAuthInput(BaseModel):
    code: str
    redirect_uri: Optional[str]
    signup_code: Optional[str]
    team_ids_to_join: Optional[List[str]]
    timezone: str


class ImageUploadFromUrlPayload(BaseModel):
    last_sync_id: float
    success: bool
    url: Optional[str]


class Integration(BaseModel):
    archived_at: Any
    created_at: Any
    creator: "User"
    id: str
    organization: "Organization"
    service: str
    team: Optional["Team"]
    updated_at: Any


class IntegrationConnection(BaseModel):
    edges: List["IntegrationEdge"]
    nodes: List["Integration"]
    page_info: "PageInfo"


class IntegrationEdge(BaseModel):
    cursor: str
    node: "Integration"


class IntegrationPayload(BaseModel):
    integration: Optional["Integration"]
    last_sync_id: float
    success: bool


class IntegrationRequestInput(BaseModel):
    email: Optional[str]
    name: str


class IntegrationRequestPayload(BaseModel):
    success: bool


class IntegrationSettings(BaseModel):
    front: Optional["FrontSettings"]
    git_hub: Optional["GitHubSettings"]
    google_sheets: Optional["GoogleSheetsSettings"]
    intercom: Optional["IntercomSettings"]
    jira: Optional["JiraSettings"]
    notion: Optional["NotionSettings"]
    sentry: Optional["SentrySettings"]
    slack_org_project_updates_post: Optional["SlackPostSettings"]
    slack_post: Optional["SlackPostSettings"]
    slack_project_post: Optional["SlackPostSettings"]
    zendesk: Optional["ZendeskSettings"]


class IntegrationSettingsInput(BaseModel):
    front: Optional["FrontSettingsInput"]
    git_hub: Optional["GitHubSettingsInput"]
    google_sheets: Optional["GoogleSheetsSettingsInput"]
    intercom: Optional["IntercomSettingsInput"]
    jira: Optional["JiraSettingsInput"]
    notion: Optional["NotionSettingsInput"]
    sentry: Optional["SentrySettingsInput"]
    slack_org_project_updates_post: Optional["SlackPostSettingsInput"]
    slack_post: Optional["SlackPostSettingsInput"]
    slack_project_post: Optional["SlackPostSettingsInput"]
    zendesk: Optional["ZendeskSettingsInput"]


class IntegrationTemplate(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    integration: "Integration"
    template: "Template"
    updated_at: Any


class IntegrationTemplateConnection(BaseModel):
    edges: List["IntegrationTemplateEdge"]
    nodes: List["IntegrationTemplate"]
    page_info: "PageInfo"


class IntegrationTemplateCreateInput(BaseModel):
    id: Optional[str]
    integration_id: str
    template_id: str


class IntegrationTemplateEdge(BaseModel):
    cursor: str
    node: "IntegrationTemplate"


class IntegrationTemplatePayload(BaseModel):
    integration_template: "IntegrationTemplate"
    last_sync_id: float
    success: bool


class IntegrationsSettings(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    project: Optional["Project"]
    slack_issue_added_to_triage: Optional[bool]
    slack_issue_created: Optional[bool]
    slack_issue_new_comment: Optional[bool]
    slack_issue_sla_breached: Optional[bool]
    slack_issue_sla_high_risk: Optional[bool]
    slack_issue_status_changed_all: Optional[bool]
    slack_issue_status_changed_done: Optional[bool]
    slack_project_update_created: Optional[bool]
    slack_project_update_created_to_team: Optional[bool]
    slack_project_update_created_to_workspace: Optional[bool]
    team: Optional["Team"]
    updated_at: Any


class IntegrationsSettingsConnection(BaseModel):
    edges: List["IntegrationsSettingsEdge"]
    nodes: List["IntegrationsSettings"]
    page_info: "PageInfo"


class IntegrationsSettingsCreateInput(BaseModel):
    id: Optional[str]
    project_id: Optional[str]
    slack_issue_added_to_triage: Optional[bool]
    slack_issue_created: Optional[bool]
    slack_issue_new_comment: Optional[bool]
    slack_issue_sla_breached: Optional[bool]
    slack_issue_sla_high_risk: Optional[bool]
    slack_issue_status_changed_all: Optional[bool]
    slack_issue_status_changed_done: Optional[bool]
    slack_project_update_created: Optional[bool]
    slack_project_update_created_to_team: Optional[bool]
    slack_project_update_created_to_workspace: Optional[bool]
    team_id: Optional[str]


class IntegrationsSettingsEdge(BaseModel):
    cursor: str
    node: "IntegrationsSettings"


class IntegrationsSettingsPayload(BaseModel):
    integrations_settings: "IntegrationsSettings"
    last_sync_id: float
    success: bool


class IntegrationsSettingsUpdateInput(BaseModel):
    slack_issue_added_to_triage: Optional[bool]
    slack_issue_created: Optional[bool]
    slack_issue_new_comment: Optional[bool]
    slack_issue_sla_breached: Optional[bool]
    slack_issue_sla_high_risk: Optional[bool]
    slack_issue_status_changed_all: Optional[bool]
    slack_issue_status_changed_done: Optional[bool]
    slack_project_update_created: Optional[bool]
    slack_project_update_created_to_team: Optional[bool]
    slack_project_update_created_to_workspace: Optional[bool]


class IntercomSettings(BaseModel):
    automate_ticket_reopening_on_cancellation: Optional[bool]
    automate_ticket_reopening_on_comment: Optional[bool]
    automate_ticket_reopening_on_completion: Optional[bool]
    send_note_on_comment: Optional[bool]
    send_note_on_status_change: Optional[bool]


class IntercomSettingsInput(BaseModel):
    automate_ticket_reopening_on_cancellation: Optional[bool]
    automate_ticket_reopening_on_comment: Optional[bool]
    automate_ticket_reopening_on_completion: Optional[bool]
    send_note_on_comment: Optional[bool]
    send_note_on_status_change: Optional[bool]




class IssueDraft(BaseModel):
    archived_at: Any
    assignee_id: Optional[str]
    attachments: Any
    created_at: Any
    creator: "User"
    cycle_id: Optional[str]
    description: Optional[str]
    description_data: Any
    due_date: Any
    estimate: Optional[float]
    id: str
    parent: Optional["IssueDraft"]
    parent_issue: Optional["Issue"]
    priority: float
    priority_label: str
    project_id: Optional[str]
    project_milestone_id: Optional[str]
    state_id: str
    sub_issue_sort_order: Optional[float]
    team_id: str
    title: str
    updated_at: Any


class IssueFilter(BaseModel):
    and_: Optional[List["IssueFilter"]]
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
    has_blocked_by_relations: Optional["RelationExistsComparator"]
    has_blocking_relations: Optional["RelationExistsComparator"]
    has_duplicate_relations: Optional["RelationExistsComparator"]
    has_related_relations: Optional["RelationExistsComparator"]
    id: Optional["IDComparator"]
    labels: Optional["IssueLabelCollectionFilter"]
    number: Optional["NumberComparator"]
    or_: Optional[List["IssueFilter"]]
    parent: Optional["NullableIssueFilter"]
    priority: Optional["NullableNumberComparator"]
    project: Optional["NullableProjectFilter"]
    project_milestone: Optional["NullableProjectMilestoneFilter"]
    searchable_content: Optional["ContentComparator"]
    sla_status: Optional["SlaStatusComparator"]
    snoozed_by: Optional["NullableUserFilter"]
    snoozed_until_at: Optional["NullableDateComparator"]
    started_at: Optional["NullableDateComparator"]
    state: Optional["WorkflowStateFilter"]
    subscribers: Optional["UserCollectionFilter"]
    team: Optional["TeamFilter"]
    title: Optional["StringComparator"]
    triaged_at: Optional["NullableDateComparator"]
    updated_at: Optional["DateComparator"]


class IssueHistory(BaseModel):
    actor: Optional["User"]
    actor_id: Optional[str]
    added_label_ids: Optional[List[str]]
    archived: Optional[bool]
    archived_at: Any
    attachment: Optional["Attachment"]
    attachment_id: Optional[str]
    auto_archived: Optional[bool]
    auto_closed: Optional[bool]
    changes: Any
    created_at: Any
    from_assignee: Optional["User"]
    from_assignee_id: Optional[str]
    from_cycle: Optional["Cycle"]
    from_cycle_id: Optional[str]
    from_due_date: Any
    from_estimate: Optional[float]
    from_parent: Optional["Issue"]
    from_parent_id: Optional[str]
    from_priority: Optional[float]
    from_project: Optional["Project"]
    from_project_id: Optional[str]
    from_state: Optional["WorkflowState"]
    from_state_id: Optional[str]
    from_team: Optional["Team"]
    from_team_id: Optional[str]
    from_title: Optional[str]
    id: str
    issue: "Issue"
    issue_import: Optional["IssueImport"]
    relation_changes: Optional[List["IssueRelationHistoryPayload"]]
    removed_label_ids: Optional[List[str]]
    to_assignee: Optional["User"]
    to_assignee_id: Optional[str]
    to_converted_project: Optional["Project"]
    to_converted_project_id: Optional[str]
    to_cycle: Optional["Cycle"]
    to_cycle_id: Optional[str]
    to_due_date: Any
    to_estimate: Optional[float]
    to_parent: Optional["Issue"]
    to_parent_id: Optional[str]
    to_priority: Optional[float]
    to_project: Optional["Project"]
    to_project_id: Optional[str]
    to_state: Optional["WorkflowState"]
    to_state_id: Optional[str]
    to_team: Optional["Team"]
    to_team_id: Optional[str]
    to_title: Optional[str]
    trashed: Optional[bool]
    updated_at: Any
    updated_description: Optional[bool]


class IssueHistoryConnection(BaseModel):
    edges: List["IssueHistoryEdge"]
    nodes: List["IssueHistory"]
    page_info: "PageInfo"


class IssueHistoryEdge(BaseModel):
    cursor: str
    node: "IssueHistory"


class IssueImport(BaseModel):
    archived_at: Any
    created_at: Any
    creator_id: str
    csv_file_url: Optional[str]
    error: Optional[str]
    id: str
    mapping: Any
    progress: Optional[float]
    service: str
    status: str
    team_name: Optional[str]
    updated_at: Any


class IssueImportDeletePayload(BaseModel):
    issue_import: Optional["IssueImport"]
    last_sync_id: float
    success: bool


class IssueImportMappingInput(BaseModel):
    epics: Any
    users: Any
    workflow_states: Any


class IssueImportPayload(BaseModel):
    issue_import: Optional["IssueImport"]
    last_sync_id: float
    success: bool


class IssueImportUpdateInput(BaseModel):
    mapping: Any




class IssueLabelCollectionFilter(BaseModel):
    and_: Optional[List["IssueLabelCollectionFilter"]]
    created_at: Optional["DateComparator"]
    creator: Optional["NullableUserFilter"]
    every: Optional["IssueLabelFilter"]
    id: Optional["IDComparator"]
    length: Optional["NumberComparator"]
    name: Optional["StringComparator"]
    or_: Optional[List["IssueLabelCollectionFilter"]]
    parent: Optional["IssueLabelFilter"]
    some: Optional["IssueLabelFilter"]
    team: Optional["TeamFilter"]
    updated_at: Optional["DateComparator"]


class IssueLabelCreateInput(BaseModel):
    color: Optional[str]
    description: Optional[str]
    id: Optional[str]
    name: str
    parent_id: Optional[str]
    team_id: Optional[str]


class IssueLabelEdge(BaseModel):
    cursor: str
    node: "IssueLabel"


class IssueLabelFilter(BaseModel):
    and_: Optional[List["IssueLabelFilter"]]
    created_at: Optional["DateComparator"]
    creator: Optional["NullableUserFilter"]
    id: Optional["IDComparator"]
    name: Optional["StringComparator"]
    or_: Optional[List["IssueLabelFilter"]]
    parent: Optional["IssueLabelFilter"]
    team: Optional["TeamFilter"]
    updated_at: Optional["DateComparator"]


class IssueLabelPayload(BaseModel):
    issue_label: "IssueLabel"
    last_sync_id: float
    success: bool


class IssueLabelUpdateInput(BaseModel):
    color: Optional[str]
    description: Optional[str]
    name: Optional[str]
    parent_id: Optional[str]


class Entity(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    updated_at: Any


class Notification(BaseModel):
    actor: Optional["User"]
    archived_at: Any
    created_at: Any
    emailed_at: Any
    id: str
    read_at: Any
    snoozed_until_at: Any
    type: str
    unsnoozed_at: Any
    updated_at: Any
    user: "User"


class IssueNotification(Entity, Node, Notification):
    actor: Optional["User"]
    archived_at: Any
    comment: Optional["Comment"]
    created_at: Any
    emailed_at: Any
    id: str
    issue: "Issue"
    reaction_emoji: Optional[str]
    read_at: Any
    snoozed_until_at: Any
    team: "Team"
    type: str
    unsnoozed_at: Any
    updated_at: Any
    user: "User"


class IssuePayload(BaseModel):
    issue: Optional["Issue"]
    last_sync_id: float
    success: bool


class IssuePriorityValue(BaseModel):
    label: str
    priority: int


class IssueRelation(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    issue: "Issue"
    related_issue: "Issue"
    type: str
    updated_at: Any


class IssueRelationConnection(BaseModel):
    edges: List["IssueRelationEdge"]
    nodes: List["IssueRelation"]
    page_info: "PageInfo"


class IssueRelationCreateInput(BaseModel):
    id: Optional[str]
    issue_id: str
    related_issue_id: str
    type: "IssueRelationType"


class IssueRelationEdge(BaseModel):
    cursor: str
    node: "IssueRelation"


class IssueRelationHistoryPayload(BaseModel):
    identifier: str
    type: str


class IssueRelationPayload(BaseModel):
    issue_relation: "IssueRelation"
    last_sync_id: float
    success: bool


class IssueRelationType(str, Enum):
    blocks = "blocks"
    duplicate = "duplicate"
    related = "related"


class IssueRelationUpdateInput(BaseModel):
    issue_id: Optional[str]
    related_issue_id: Optional[str]
    type: Optional[str]


class IssueUpdateInput(BaseModel):
    assignee_id: Optional[str]
    board_order: Optional[float]
    cycle_id: Optional[str]
    description: Optional[str]
    description_data: Any
    due_date: Any
    estimate: Optional[int]
    label_ids: Optional[List[str]]
    parent_id: Optional[str]
    priority: Optional[int]
    project_id: Optional[str]
    project_milestone_id: Optional[str]
    sla_breaches_at: Any
    snoozed_by_id: Optional[str]
    snoozed_until_at: Any
    sort_order: Optional[float]
    state_id: Optional[str]
    sub_issue_sort_order: Optional[float]
    subscriber_ids: Optional[List[str]]
    team_id: Optional[str]
    title: Optional[str]
    trashed: Optional[bool]


class JiraConfigurationInput(BaseModel):
    access_token: str
    email: str
    hostname: str
    project: Optional[str]


class JiraLinearMapping(BaseModel):
    jira_project_id: str
    linear_team_id: str


class JiraLinearMappingInput(BaseModel):
    jira_project_id: str
    linear_team_id: str


class JiraProjectData(BaseModel):
    id: str
    key: str
    name: str


class JiraProjectDataInput(BaseModel):
    id: str
    key: str
    name: str


class JiraSettings(BaseModel):
    project_mapping: Optional[List["JiraLinearMapping"]]
    projects: List["JiraProjectData"]


class JiraSettingsInput(BaseModel):
    project_mapping: Optional[List["JiraLinearMappingInput"]]
    projects: List["JiraProjectDataInput"]


class JoinOrganizationInput(BaseModel):
    organization_id: str


class LogoutResponse(BaseModel):
    success: bool


class Mutation(BaseModel):
    airbyte_integration_connect: "IntegrationPayload"
    api_key_create: "ApiKeyPayload"
    api_key_delete: "ArchivePayload"
    attachment_create: "AttachmentPayload"
    attachment_delete: "ArchivePayload"
    attachment_link_discord: "AttachmentPayload"
    attachment_link_front: "FrontAttachmentPayload"
    attachment_link_intercom: "AttachmentPayload"
    attachment_link_jira_issue: "AttachmentPayload"
    attachment_link_url: "AttachmentPayload"
    attachment_link_zendesk: "AttachmentPayload"
    attachment_update: "AttachmentPayload"
    comment_create: "CommentPayload"
    comment_delete: "ArchivePayload"
    comment_update: "CommentPayload"
    contact_create: "ContactPayload"
    contact_sales_create: "ContactPayload"
    create_csv_export_report: "CreateCsvExportReportPayload"
    create_organization_from_onboarding: "CreateOrJoinOrganizationResponse"
    custom_view_create: "CustomViewPayload"
    custom_view_delete: "ArchivePayload"
    custom_view_update: "CustomViewPayload"
    cycle_archive: "ArchivePayload"
    cycle_create: "CyclePayload"
    cycle_update: "CyclePayload"
    document_create: "DocumentPayload"
    document_delete: "ArchivePayload"
    document_update: "DocumentPayload"
    email_subscribe: "EmailSubscribePayload"
    email_token_user_account_auth: "AuthResolverResponse"
    email_unsubscribe: "EmailUnsubscribePayload"
    email_user_account_auth_challenge: "EmailUserAccountAuthChallengeResponse"
    emoji_create: "EmojiPayload"
    emoji_delete: "ArchivePayload"
    event_create: "EventPayload"
    favorite_create: "FavoritePayload"
    favorite_delete: "ArchivePayload"
    favorite_update: "FavoritePayload"
    file_upload: "UploadPayload"
    google_user_account_auth: "AuthResolverResponse"
    image_upload_from_url: "ImageUploadFromUrlPayload"
    integration_delete: "ArchivePayload"
    integration_discord: "IntegrationPayload"
    integration_figma: "IntegrationPayload"
    integration_front: "IntegrationPayload"
    integration_github_commit_create: "GitHubCommitIntegrationPayload"
    integration_github_connect: "IntegrationPayload"
    integration_gitlab_connect: "IntegrationPayload"
    integration_google_sheets: "IntegrationPayload"
    integration_intercom: "IntegrationPayload"
    integration_intercom_delete: "IntegrationPayload"
    integration_request: "IntegrationRequestPayload"
    integration_sentry_connect: "IntegrationPayload"
    integration_settings_update: "IntegrationPayload"
    integration_slack: "IntegrationPayload"
    integration_slack_import_emojis: "IntegrationPayload"
    integration_slack_intake: "IntegrationPayload"
    integration_slack_org_project_updates_post: "IntegrationPayload"
    integration_slack_personal: "IntegrationPayload"
    integration_slack_post: "IntegrationPayload"
    integration_slack_project_post: "IntegrationPayload"
    integration_template_create: "IntegrationTemplatePayload"
    integration_template_delete: "ArchivePayload"
    integration_zendesk: "IntegrationPayload"
    integrations_settings_create: "IntegrationsSettingsPayload"
    integrations_settings_update: "IntegrationsSettingsPayload"
    issue_archive: "ArchivePayload"
    issue_batch_update: "IssueBatchPayload"
    issue_create: "IssuePayload"
    issue_delete: "ArchivePayload"
    issue_description_update_from_front: "IssuePayload"
    issue_import_create_asana: "IssueImportPayload"
    issue_import_create_clubhouse: "IssueImportPayload"
    issue_import_create_github: "IssueImportPayload"
    issue_import_create_jira: "IssueImportPayload"
    issue_import_delete: "IssueImportDeletePayload"
    issue_import_process: "IssueImportPayload"
    issue_import_update: "IssueImportPayload"
    issue_label_create: "IssueLabelPayload"
    issue_label_delete: "ArchivePayload"
    issue_label_update: "IssueLabelPayload"
    issue_relation_create: "IssueRelationPayload"
    issue_relation_delete: "ArchivePayload"
    issue_relation_update: "IssueRelationPayload"
    issue_reminder: "IssuePayload"
    issue_unarchive: "ArchivePayload"
    issue_update: "IssuePayload"
    jira_integration_connect: "IntegrationPayload"
    join_organization_from_onboarding: "CreateOrJoinOrganizationResponse"
    leave_organization: "CreateOrJoinOrganizationResponse"
    logout: "LogoutResponse"
    notification_archive: "ArchivePayload"
    notification_subscription_create: "NotificationSubscriptionPayload"
    notification_subscription_delete: "ArchivePayload"
    notification_subscription_update: "NotificationSubscriptionPayload"
    notification_unarchive: "ArchivePayload"
    notification_update: "NotificationPayload"
    organization_cancel_delete: "OrganizationCancelDeletePayload"
    organization_delete: "OrganizationDeletePayload"
    organization_delete_challenge: "OrganizationDeletePayload"
    organization_domain_claim: "OrganizationDomainSimplePayload"
    organization_domain_create: "OrganizationDomainPayload"
    organization_domain_delete: "ArchivePayload"
    organization_domain_verify: "OrganizationDomainPayload"
    organization_invite_create: "OrganizationInvitePayload"
    organization_invite_delete: "ArchivePayload"
    organization_invite_update: "OrganizationInvitePayload"
    organization_start_plus_trial: "OrganizationStartPlusTrialPayload"
    organization_update: "OrganizationPayload"
    project_create: "ProjectPayload"
    project_delete: "ArchivePayload"
    project_link_create: "ProjectLinkPayload"
    project_link_delete: "ArchivePayload"
    project_link_update: "ProjectLinkPayload"
    project_milestone_create: "ProjectMilestonePayload"
    project_milestone_delete: "ArchivePayload"
    project_milestone_update: "ProjectMilestonePayload"
    project_unarchive: "ArchivePayload"
    project_update: "ProjectPayload"
    project_update_create: "ProjectUpdatePayload"
    project_update_delete: "ArchivePayload"
    project_update_interaction_create: "ProjectUpdateInteractionPayload"
    project_update_mark_as_read: "ProjectUpdateWithInteractionPayload"
    project_update_update: "ProjectUpdatePayload"
    push_subscription_create: "PushSubscriptionPayload"
    push_subscription_delete: "PushSubscriptionPayload"
    reaction_create: "ReactionPayload"
    reaction_delete: "ArchivePayload"
    refresh_google_sheets_data: "IntegrationPayload"
    resend_organization_invite: "ArchivePayload"
    roadmap_archive: "ArchivePayload"
    roadmap_create: "RoadmapPayload"
    roadmap_delete: "ArchivePayload"
    roadmap_to_project_create: "RoadmapToProjectPayload"
    roadmap_to_project_delete: "ArchivePayload"
    roadmap_to_project_update: "RoadmapToProjectPayload"
    roadmap_unarchive: "ArchivePayload"
    roadmap_update: "RoadmapPayload"
    saml_token_user_account_auth: "AuthResolverResponse"
    team_create: "TeamPayload"
    team_cycles_delete: "TeamPayload"
    team_delete: "ArchivePayload"
    team_key_delete: "ArchivePayload"
    team_membership_create: "TeamMembershipPayload"
    team_membership_delete: "ArchivePayload"
    team_membership_update: "TeamMembershipPayload"
    team_update: "TeamPayload"
    template_create: "TemplatePayload"
    template_delete: "ArchivePayload"
    template_update: "TemplatePayload"
    user_demote_admin: "UserAdminPayload"
    user_demote_member: "UserAdminPayload"
    user_discord_connect: "UserPayload"
    user_external_user_disconnect: "UserPayload"
    user_flag_update: "UserSettingsFlagPayload"
    user_git_hub_connect: "UserPayload"
    user_google_calendar_connect: "UserPayload"
    user_promote_admin: "UserAdminPayload"
    user_promote_member: "UserAdminPayload"
    user_settings_flag_increment: "UserSettingsFlagPayload"
    user_settings_flags_reset: "UserSettingsFlagsResetPayload"
    user_settings_update: "UserSettingsPayload"
    user_suspend: "UserAdminPayload"
    user_unsuspend: "UserAdminPayload"
    user_update: "UserPayload"
    view_preferences_create: "ViewPreferencesPayload"
    view_preferences_delete: "ArchivePayload"
    view_preferences_update: "ViewPreferencesPayload"
    webhook_create: "WebhookPayload"
    webhook_delete: "ArchivePayload"
    webhook_update: "WebhookPayload"
    workflow_state_archive: "ArchivePayload"
    workflow_state_create: "WorkflowStatePayload"
    workflow_state_update: "WorkflowStatePayload"


class NotificationConnection(BaseModel):
    edges: List["NotificationEdge"]
    nodes: List["Notification"]
    page_info: "PageInfo"


class NotificationEdge(BaseModel):
    cursor: str
    node: "Notification"


class NotificationPayload(BaseModel):
    last_sync_id: float
    notification: "Notification"
    success: bool


class NotificationSubscriptionConnection(BaseModel):
    edges: List["NotificationSubscriptionEdge"]
    nodes: List["NotificationSubscription"]
    page_info: "PageInfo"


class NotificationSubscriptionCreateInput(BaseModel):
    id: Optional[str]
    project_id: Optional[str]
    project_notification_subscription_type: Optional[
        "ProjectNotificationSubscriptionType"
    ]
    team_id: Optional[str]
    team_notification_subscription_types: Optional[List[str]]


class NotificationSubscriptionEdge(BaseModel):
    cursor: str
    node: "NotificationSubscription"


class NotificationSubscriptionPayload(BaseModel):
    last_sync_id: float
    notification_subscription: "NotificationSubscription"
    success: bool


class NotificationSubscriptionUpdateInput(BaseModel):
    project_notification_subscription_type: Optional[
        "ProjectNotificationSubscriptionType"
    ]
    team_notification_subscription_types: Optional[List[str]]


class NotificationUpdateInput(BaseModel):
    project_update_id: Optional[str]
    read_at: Any
    snoozed_until_at: Any


class NotionSettings(BaseModel):
    workspace_id: str
    workspace_name: str


class NotionSettingsInput(BaseModel):
    workspace_id: str
    workspace_name: str


class NumberComparator(BaseModel):
    eq: Optional[float]
    gt: Optional[float]
    gte: Optional[float]
    in_: Optional[List[float]]
    lt: Optional[float]
    lte: Optional[float]
    neq: Optional[float]
    nin: Optional[List[float]]


class OAuthClientApprovalStatus(str, Enum):
    approved = "approved"
    denied = "denied"
    requested = "requested"


class OauthClient(BaseModel):
    archived_at: Any
    client_id: str
    client_secret: str
    created_at: Any
    creator: "User"
    description: Optional[str]
    developer: str
    developer_url: str
    id: str
    image_url: Optional[str]
    name: str
    organization: "Organization"
    public_enabled: bool
    redirect_uris: List[str]
    updated_at: Any
    webhook_resource_types: List[str]
    webhook_secret: Optional[str]
    webhook_url: Optional[str]


class OauthClientApproval(BaseModel):
    archived_at: Any
    created_at: Any
    deny_reason: Optional[str]
    id: str
    oauth_client_id: str
    request_reason: Optional[str]
    requester_id: str
    responder_id: Optional[str]
    scopes: List[str]
    status: "OAuthClientApprovalStatus"
    updated_at: Any


class OauthClientApprovalNotification(Entity, Node, Notification):
    actor: Optional["User"]
    archived_at: Any
    created_at: Any
    emailed_at: Any
    id: str
    oauth_client_approval: "OauthClientApproval"
    read_at: Any
    snoozed_until_at: Any
    type: str
    unsnoozed_at: Any
    updated_at: Any
    user: "User"


class OauthClientConnection(BaseModel):
    edges: List["OauthClientEdge"]
    nodes: List["OauthClient"]
    page_info: "PageInfo"


class OauthClientEdge(BaseModel):
    cursor: str
    node: "OauthClient"


class OnboardingCustomerSurvey(BaseModel):
    company_role: Optional[str]
    company_size: Optional[str]


class Organization(BaseModel):
    allowed_auth_services: List[str]
    archived_at: Any
    created_at: Any
    created_issue_count: int
    deletion_requested_at: Any
    git_branch_format: Optional[str]
    git_linkback_messages_enabled: bool
    git_public_linkback_messages_enabled: bool
    id: str
    integrations: "IntegrationConnection"
    labels: "IssueLabelConnection"
    logo_url: Optional[str]
    name: str
    period_upload_volume: float
    previous_url_keys: List[str]
    project_update_reminders_day: "Day"
    project_update_reminders_hour: float
    project_updates_reminder_frequency: "ProjectUpdateReminderFrequency"
    release_channel: "ReleaseChannel"
    roadmap_enabled: bool
    saml_enabled: bool
    scim_enabled: bool
    subscription: Optional["PaidSubscription"]
    teams: "TeamConnection"
    templates: "TemplateConnection"
    trial_ends_at: Any
    updated_at: Any
    url_key: str
    user_count: int
    users: "UserConnection"


class OrganizationCancelDeletePayload(BaseModel):
    success: bool


class OrganizationDeletePayload(BaseModel):
    success: bool


class OrganizationDomain(BaseModel):
    archived_at: Any
    auth_type: "OrganizationDomainAuthType"
    claimed: Optional[bool]
    created_at: Any
    creator: Optional["User"]
    id: str
    name: str
    updated_at: Any
    verification_email: Optional[str]
    verified: bool


class OrganizationDomainAuthType(str, Enum):
    general = "general"
    saml = "saml"


class OrganizationDomainClaimPayload(BaseModel):
    verification_string: str


class OrganizationDomainCreateInput(BaseModel):
    auth_type: Optional[str]
    id: Optional[str]
    name: str
    verification_email: Optional[str]


class OrganizationDomainPayload(BaseModel):
    last_sync_id: float
    organization_domain: "OrganizationDomain"
    success: bool


class OrganizationDomainSimplePayload(BaseModel):
    success: bool


class OrganizationDomainVerificationInput(BaseModel):
    organization_domain_id: str
    verification_code: str


class OrganizationExistsPayload(BaseModel):
    exists: bool
    success: bool


class OrganizationInvite(BaseModel):
    accepted_at: Any
    archived_at: Any
    created_at: Any
    email: str
    expires_at: Any
    external: bool
    id: str
    invitee: Optional["User"]
    inviter: "User"
    organization: "Organization"
    role: "UserRoleType"
    updated_at: Any


class OrganizationInviteConnection(BaseModel):
    edges: List["OrganizationInviteEdge"]
    nodes: List["OrganizationInvite"]
    page_info: "PageInfo"


class OrganizationInviteCreateInput(BaseModel):
    email: str
    id: Optional[str]
    message: Optional[str]
    role: Optional["UserRoleType"]
    team_ids: Optional[List[str]]


class OrganizationInviteDetailsPayload(BaseModel):
    accepted: bool
    created_at: Any
    email: str
    expired: bool
    inviter: str
    organization_id: str
    organization_logo_url: Optional[str]
    organization_name: str
    role: "UserRoleType"


class OrganizationInviteEdge(BaseModel):
    cursor: str
    node: "OrganizationInvite"


class OrganizationInvitePayload(BaseModel):
    last_sync_id: float
    organization_invite: "OrganizationInvite"
    success: bool


class OrganizationInviteUpdateInput(BaseModel):
    team_ids: List[str]


class OrganizationPayload(BaseModel):
    last_sync_id: float
    organization: Optional["Organization"]
    success: bool


class OrganizationStartPlusTrialPayload(BaseModel):
    success: bool


class PaginationOrderBy(str, Enum):
    createdAt = "createdAt"
    updatedAt = "updatedAt"


class PaidSubscription(BaseModel):
    archived_at: Any
    canceled_at: Any
    created_at: Any
    creator: Optional["User"]
    id: str
    next_billing_at: Any
    organization: "Organization"
    pending_change_type: Optional[str]
    seats: float
    seats_maximum: Optional[float]
    seats_minimum: Optional[float]
    type: str
    updated_at: Any


class PersonalNote(BaseModel):
    archived_at: Any
    content_data: Any
    created_at: Any
    id: str
    updated_at: Any
    user: "User"


class ProjectCollectionFilter(BaseModel):
    and_: Optional[List["ProjectCollectionFilter"]]
    created_at: Optional["DateComparator"]
    creator: Optional["UserFilter"]
    every: Optional["ProjectFilter"]
    id: Optional["IDComparator"]
    issues: Optional["IssueCollectionFilter"]
    lead: Optional["NullableUserFilter"]
    length: Optional["NumberComparator"]
    members: Optional["UserFilter"]
    name: Optional["StringComparator"]
    or_: Optional[List["ProjectCollectionFilter"]]
    roadmaps: Optional["RoadmapCollectionFilter"]
    slug_id: Optional["StringComparator"]
    some: Optional["ProjectFilter"]
    start_date: Optional["NullableDateComparator"]
    state: Optional["StringComparator"]
    target_date: Optional["NullableDateComparator"]
    updated_at: Optional["DateComparator"]


class ProjectConnection(BaseModel):
    edges: List["ProjectEdge"]
    nodes: List["Project"]
    page_info: "PageInfo"


class ProjectCreateInput(BaseModel):
    color: Optional[str]
    converted_from_issue_id: Optional[str]
    description: Optional[str]
    icon: Optional[str]
    id: Optional[str]
    lead_id: Optional[str]
    member_ids: Optional[List[str]]
    name: str
    sort_order: Optional[float]
    start_date: Any
    state: Optional[str]
    target_date: Any
    team_ids: List[str]


class ProjectEdge(BaseModel):
    cursor: str
    node: "Project"


class ProjectFilter(BaseModel):
    and_: Optional[List["ProjectFilter"]]
    created_at: Optional["DateComparator"]
    creator: Optional["UserFilter"]
    id: Optional["IDComparator"]
    issues: Optional["IssueCollectionFilter"]
    lead: Optional["NullableUserFilter"]
    members: Optional["UserFilter"]
    name: Optional["StringComparator"]
    or_: Optional[List["ProjectFilter"]]
    roadmaps: Optional["RoadmapCollectionFilter"]
    slug_id: Optional["StringComparator"]
    start_date: Optional["NullableDateComparator"]
    state: Optional["StringComparator"]
    target_date: Optional["NullableDateComparator"]
    updated_at: Optional["DateComparator"]


class ProjectLink(BaseModel):
    archived_at: Any
    created_at: Any
    creator: "User"
    id: str
    label: str
    project: "Project"
    updated_at: Any
    url: str


class ProjectLinkConnection(BaseModel):
    edges: List["ProjectLinkEdge"]
    nodes: List["ProjectLink"]
    page_info: "PageInfo"


class ProjectLinkCreateInput(BaseModel):
    id: Optional[str]
    label: str
    project_id: str
    url: str


class ProjectLinkEdge(BaseModel):
    cursor: str
    node: "ProjectLink"


class ProjectLinkPayload(BaseModel):
    last_sync_id: float
    project_link: "ProjectLink"
    success: bool


class ProjectLinkUpdateInput(BaseModel):
    label: Optional[str]
    url: Optional[str]


class ProjectMilestoneEdge(BaseModel):
    cursor: str
    node: "ProjectMilestone"


class ProjectMilestonePayload(BaseModel):
    last_sync_id: float
    project_milestone: "ProjectMilestone"
    success: bool


class ProjectMilestoneUpdateInput(BaseModel):
    description: Optional[str]
    name: Optional[str]
    project_id: Optional[str]
    sort_order: Optional[float]
    target_date: Any


class ProjectNotification(Entity, Node, Notification):
    actor: Optional["User"]
    archived_at: Any
    created_at: Any
    emailed_at: Any
    id: str
    project: "Project"
    project_update: Optional["ProjectUpdate"]
    read_at: Any
    snoozed_until_at: Any
    type: str
    unsnoozed_at: Any
    updated_at: Any
    user: "User"


class Team(BaseModel):
    active_cycle: Optional["Cycle"]
    archived_at: Any
    auto_archive_period: float
    auto_close_period: Optional[float]
    auto_close_state_id: Optional[str]
    color: Optional[str]
    created_at: Any
    cycle_calender_url: str
    cycle_cooldown_time: float
    cycle_duration: float
    cycle_issue_auto_assign_completed: bool
    cycle_issue_auto_assign_started: bool
    cycle_lock_to_active: bool
    cycle_start_day: float
    cycles: "CycleConnection"
    cycles_enabled: bool
    default_issue_estimate: float
    default_issue_state: Optional["WorkflowState"]
    default_template_for_members: Optional["Template"]
    default_template_for_non_members: Optional["Template"]
    description: Optional[str]
    draft_workflow_state: Optional["WorkflowState"]
    group_issue_history: bool
    icon: Optional[str]
    id: str
    integrations_settings: Optional["IntegrationsSettings"]
    invite_hash: str
    issue_estimation_allow_zero: bool
    issue_estimation_extended: bool
    issue_estimation_type: str
    issue_ordering_no_priority_first: bool
    issue_sort_order_default_to_bottom: bool
    issues: "IssueConnection"
    key: str
    labels: "IssueLabelConnection"
    marked_as_duplicate_workflow_state: Optional["WorkflowState"]
    members: "UserConnection"
    memberships: "TeamMembershipConnection"
    merge_workflow_state: Optional["WorkflowState"]
    name: str
    organization: "Organization"
    private: bool
    projects: "ProjectConnection"
    require_priority_to_leave_triage: bool
    review_workflow_state: Optional["WorkflowState"]
    slack_issue_comments: bool
    slack_issue_statuses: bool
    slack_new_issue: bool
    start_workflow_state: Optional["WorkflowState"]
    states: "WorkflowStateConnection"
    templates: "TemplateConnection"
    timezone: str
    triage_enabled: bool
    triage_issue_state: Optional["WorkflowState"]
    upcoming_cycle_count: float
    updated_at: Any
    webhooks: "WebhookConnection"


class NotificationSubscription(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    project: Optional["Project"]
    team: Optional["Team"]
    type: str
    updated_at: Any
    user: "User"


class ProjectNotificationSubscription(Entity, Node, NotificationSubscription):
    archived_at: Any
    created_at: Any
    id: str
    project: "Project"
    project_notification_subscription_type: "ProjectNotificationSubscriptionType"
    team: Optional["Team"]
    type: str
    updated_at: Any
    user: "User"


class ProjectNotificationSubscriptionType(str, Enum):
    all = "all"
    custom = "custom"
    importantOnly = "importantOnly"


class ProjectPayload(BaseModel):
    last_sync_id: float
    project: Optional["Project"]
    success: bool


class ProjectUpdate(BaseModel):
    archived_at: Any
    body: str
    created_at: Any
    edited_at: Any
    health: "ProjectUpdateHealthType"
    id: str
    project: "Project"
    updated_at: Any
    url: str
    user: "User"


class ProjectUpdateConnection(BaseModel):
    edges: List["ProjectUpdateEdge"]
    nodes: List["ProjectUpdate"]
    page_info: "PageInfo"


class ProjectUpdateCreateInput(BaseModel):
    body: Optional[str]
    body_data: Any
    health: Optional["ProjectUpdateHealthType"]
    id: Optional[str]
    project_id: str


class ProjectUpdateEdge(BaseModel):
    cursor: str
    node: "ProjectUpdate"


class ProjectUpdateHealthType(str, Enum):
    atRisk = "atRisk"
    offTrack = "offTrack"
    onTrack = "onTrack"


class ProjectUpdateInput(BaseModel):
    canceled_at: Any
    color: Optional[str]
    completed_at: Any
    converted_from_issue_id: Optional[str]
    description: Optional[str]
    icon: Optional[str]
    lead_id: Optional[str]
    member_ids: Optional[List[str]]
    name: Optional[str]
    project_update_reminders_paused_until_at: Any
    slack_issue_comments: Optional[bool]
    slack_issue_statuses: Optional[bool]
    slack_new_issue: Optional[bool]
    sort_order: Optional[float]
    start_date: Any
    state: Optional[str]
    target_date: Any
    team_ids: Optional[List[str]]


class ProjectUpdateInteraction(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    project_update: "ProjectUpdate"
    read_at: Any
    updated_at: Any
    user: "User"


class ProjectUpdateInteractionConnection(BaseModel):
    edges: List["ProjectUpdateInteractionEdge"]
    nodes: List["ProjectUpdateInteraction"]
    page_info: "PageInfo"


class ProjectUpdateInteractionCreateInput(BaseModel):
    id: Optional[str]
    project_update_id: str
    read_at: Any


class ProjectUpdateInteractionEdge(BaseModel):
    cursor: str
    node: "ProjectUpdateInteraction"


class ProjectUpdateInteractionPayload(BaseModel):
    last_sync_id: float
    project_update_interaction: "ProjectUpdateInteraction"
    success: bool


class ProjectUpdatePayload(BaseModel):
    last_sync_id: float
    project_update: "ProjectUpdate"
    success: bool


class ProjectUpdateReminderFrequency(str, Enum):
    never = "never"
    twoWeeks = "twoWeeks"
    week = "week"


class ProjectUpdateUpdateInput(BaseModel):
    body: Optional[str]
    body_data: Any
    health: Optional["ProjectUpdateHealthType"]


class ProjectUpdateWithInteractionPayload(BaseModel):
    interaction: "ProjectUpdateInteraction"
    last_sync_id: float
    project_update: "ProjectUpdate"
    success: bool


class PushSubscription(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    updated_at: Any


class PushSubscriptionConnection(BaseModel):
    edges: List["PushSubscriptionEdge"]
    nodes: List["PushSubscription"]
    page_info: "PageInfo"


class PushSubscriptionCreateInput(BaseModel):
    data: str
    id: Optional[str]
    type: Optional["PushSubscriptionType"]
    user_id: str


class PushSubscriptionEdge(BaseModel):
    cursor: str
    node: "PushSubscription"


class PushSubscriptionPayload(BaseModel):
    last_sync_id: float
    success: bool


class PushSubscriptionTestPayload(BaseModel):
    success: bool


class PushSubscriptionType(str, Enum):
    apple = "apple"
    web = "web"


class Query(BaseModel):
    project_milestone: "ProjectMilestone"
    project_milestones: "ProjectMilestoneConnection"
    administrable_teams: "TeamConnection"
    api_keys: "ApiKeyConnection"
    application_info: "Application"
    application_info_by_ids: List["Application"]
    application_with_authorization: "UserAuthorizedApplication"
    attachment: "Attachment"
    attachments: "AttachmentConnection"
    attachments_for_url: "AttachmentConnection"
    audit_entries: "AuditEntryConnection"
    audit_entry_types: List["AuditEntryType"]
    authorized_applications: List["AuthorizedApplication"]
    available_users: "AuthResolverResponse"
    comment: "Comment"
    comments: "CommentConnection"
    custom_view: "CustomView"
    custom_view_suggestion: "CustomViewSuggestionPayload"
    custom_views: "CustomViewConnection"
    cycle: "Cycle"
    cycles: "CycleConnection"
    document: "Document"
    documents: "DocumentConnection"
    emoji: "Emoji"
    emojis: "EmojiConnection"
    external_user: "ExternalUser"
    external_users: "ExternalUserConnection"
    favorite: "Favorite"
    favorites: "FavoriteConnection"
    figma_embed_info: "FigmaEmbedPayload"
    integration: "Integration"
    integration_template: "IntegrationTemplate"
    integration_templates: "IntegrationTemplateConnection"
    integrations: "IntegrationConnection"
    integrations_settings: "IntegrationsSettings"
    issue: "Issue"
    issue_import_finish_github_o_auth: "GithubOAuthTokenPayload"
    issue_label: "IssueLabel"
    issue_labels: "IssueLabelConnection"
    issue_priority_values: List["IssuePriorityValue"]
    issue_relation: "IssueRelation"
    issue_relations: "IssueRelationConnection"
    issue_search: "IssueConnection"
    issue_vcs_branch_search: Optional["Issue"]
    issues: "IssueConnection"
    notification: "Notification"
    notification_subscription: "NotificationSubscription"
    notification_subscriptions: "NotificationSubscriptionConnection"
    notifications: "NotificationConnection"
    organization: "Organization"
    organization_domain_claim_request: "OrganizationDomainClaimPayload"
    organization_exists: "OrganizationExistsPayload"
    organization_invite: "OrganizationInvite"
    organization_invite_details: "OrganizationInviteDetailsPayload"
    organization_invites: "OrganizationInviteConnection"
    project: "Project"
    project_link: "ProjectLink"
    project_links: "ProjectLinkConnection"
    project_update: "ProjectUpdate"
    project_update_interaction: "ProjectUpdateInteraction"
    project_update_interactions: "ProjectUpdateInteractionConnection"
    project_updates: "ProjectUpdateConnection"
    projects: "ProjectConnection"
    push_subscription_test: "PushSubscriptionTestPayload"
    rate_limit_status: "RateLimitPayload"
    roadmap: "Roadmap"
    roadmap_to_project: "RoadmapToProject"
    roadmap_to_projects: "RoadmapToProjectConnection"
    roadmaps: "RoadmapConnection"
    sso_url_from_email: "SsoUrlFromEmailResponse"
    team: "Team"
    team_membership: "TeamMembership"
    team_memberships: "TeamMembershipConnection"
    teams: "TeamConnection"
    template: "Template"
    templates: List["Template"]
    user: "User"
    user_account_exists: Optional["UserAccountExistsPayload"]
    user_settings: "UserSettings"
    users: "UserConnection"
    viewer: "User"
    webhook: "Webhook"
    webhooks: "WebhookConnection"
    workflow_state: "WorkflowState"
    workflow_states: "WorkflowStateConnection"
    workspace_authorized_applications: List["WorkspaceAuthorizedApplication"]


class RateLimitPayload(BaseModel):
    identifier: Optional[str]
    kind: str
    limits: List["RateLimitResultPayload"]


class RateLimitResultPayload(BaseModel):
    allowed_amount: float
    period: float
    remaining_amount: float
    requested_amount: float
    reset: float
    type: str


class Reaction(BaseModel):
    archived_at: Any
    created_at: Any
    emoji: str
    id: str
    updated_at: Any
    user: Optional["User"]


class ReactionConnection(BaseModel):
    edges: List["ReactionEdge"]
    nodes: List["Reaction"]
    page_info: "PageInfo"


class ReactionCreateInput(BaseModel):
    comment_id: Optional[str]
    emoji: Optional[str]
    id: Optional[str]
    project_update_id: Optional[str]


class ReactionEdge(BaseModel):
    cursor: str
    node: "Reaction"


class ReactionPayload(BaseModel):
    last_sync_id: float
    reaction: "Reaction"
    success: bool


class RelationExistsComparator(BaseModel):
    eq: Optional[bool]
    neq: Optional[bool]


class ReleaseChannel(str, Enum):
    beta = "beta"
    internal = "internal"
    preRelease = "preRelease"
    public = "public"


class Roadmap(BaseModel):
    archived_at: Any
    color: Optional[str]
    created_at: Any
    creator: "User"
    description: Optional[str]
    id: str
    name: str
    organization: "Organization"
    owner: "User"
    projects: "ProjectConnection"
    slug_id: str
    sort_order: float
    updated_at: Any


class RoadmapCollectionFilter(BaseModel):
    and_: Optional[List["RoadmapCollectionFilter"]]
    created_at: Optional["DateComparator"]
    creator: Optional["UserFilter"]
    every: Optional["RoadmapFilter"]
    id: Optional["IDComparator"]
    length: Optional["NumberComparator"]
    name: Optional["StringComparator"]
    or_: Optional[List["RoadmapCollectionFilter"]]
    slug_id: Optional["StringComparator"]
    some: Optional["RoadmapFilter"]
    updated_at: Optional["DateComparator"]


class RoadmapConnection(BaseModel):
    edges: List["RoadmapEdge"]
    nodes: List["Roadmap"]
    page_info: "PageInfo"


class RoadmapCreateInput(BaseModel):
    color: Optional[str]
    description: Optional[str]
    id: Optional[str]
    name: str
    owner_id: Optional[str]
    sort_order: Optional[float]


class RoadmapEdge(BaseModel):
    cursor: str
    node: "Roadmap"


class RoadmapFilter(BaseModel):
    and_: Optional[List["RoadmapFilter"]]
    created_at: Optional["DateComparator"]
    creator: Optional["UserFilter"]
    id: Optional["IDComparator"]
    name: Optional["StringComparator"]
    or_: Optional[List["RoadmapFilter"]]
    slug_id: Optional["StringComparator"]
    updated_at: Optional["DateComparator"]


class RoadmapPayload(BaseModel):
    last_sync_id: float
    roadmap: "Roadmap"
    success: bool


class RoadmapToProject(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    project: "Project"
    roadmap: "Roadmap"
    sort_order: str
    updated_at: Any


class RoadmapToProjectConnection(BaseModel):
    edges: List["RoadmapToProjectEdge"]
    nodes: List["RoadmapToProject"]
    page_info: "PageInfo"


class RoadmapToProjectCreateInput(BaseModel):
    id: Optional[str]
    project_id: str
    roadmap_id: str
    sort_order: Optional[float]


class RoadmapToProjectEdge(BaseModel):
    cursor: str
    node: "RoadmapToProject"


class RoadmapToProjectPayload(BaseModel):
    last_sync_id: float
    roadmap_to_project: "RoadmapToProject"
    success: bool


class RoadmapToProjectUpdateInput(BaseModel):
    sort_order: Optional[float]


class RoadmapUpdateInput(BaseModel):
    color: Optional[str]
    description: Optional[str]
    name: Optional[str]
    owner_id: Optional[str]
    sort_order: Optional[float]


class SamlConfiguration(BaseModel):
    issuer_entity_id: Optional[str]
    sso_binding: Optional[str]
    sso_endpoint: Optional[str]
    sso_sign_algo: Optional[str]
    sso_signing_cert: Optional[str]


class SamlConfigurationInput(BaseModel):
    issuer_entity_id: Optional[str]
    sso_binding: Optional[str]
    sso_endpoint: Optional[str]
    sso_sign_algo: Optional[str]
    sso_signing_cert: Optional[str]


class SamlConfigurationPayload(BaseModel):
    issuer_entity_id: Optional[str]
    sso_binding: Optional[str]
    sso_endpoint: Optional[str]
    sso_sign_algo: Optional[str]


class SentrySettings(BaseModel):
    organization_slug: str


class SentrySettingsInput(BaseModel):
    organization_slug: str


class SlaStatus(str, Enum):
    Breached = "Breached"
    Completed = "Completed"
    Failed = "Failed"
    HighRisk = "HighRisk"
    LowRisk = "LowRisk"
    MediumRisk = "MediumRisk"


class SlaStatusComparator(BaseModel):
    eq: Optional["SlaStatus"]
    in_: Optional[List["SlaStatus"]]
    neq: Optional["SlaStatus"]
    nin: Optional[List["SlaStatus"]]
    null: Optional[bool]


class SlackPostSettings(BaseModel):
    channel: str
    channel_id: str
    configuration_url: str


class SlackPostSettingsInput(BaseModel):
    channel: str
    channel_id: str
    configuration_url: str


class SourceTypeComparator(BaseModel):
    contains: Optional[str]
    contains_ignore_case: Optional[str]
    ends_with: Optional[str]
    eq: Optional[str]
    eq_ignore_case: Optional[str]
    in_: Optional[List[str]]
    neq: Optional[str]
    neq_ignore_case: Optional[str]
    nin: Optional[List[str]]
    not_contains: Optional[str]
    not_contains_ignore_case: Optional[str]
    not_ends_with: Optional[str]
    not_starts_with: Optional[str]
    starts_with: Optional[str]


class SsoUrlFromEmailResponse(BaseModel):
    saml_sso_url: str
    success: bool


class StringComparator(BaseModel):
    contains: Optional[str]
    contains_ignore_case: Optional[str]
    ends_with: Optional[str]
    eq: Optional[str]
    eq_ignore_case: Optional[str]
    in_: Optional[List[str]]
    neq: Optional[str]
    neq_ignore_case: Optional[str]
    nin: Optional[List[str]]
    not_contains: Optional[str]
    not_contains_ignore_case: Optional[str]
    not_ends_with: Optional[str]
    not_starts_with: Optional[str]
    starts_with: Optional[str]


class SyncResponse(BaseModel):
    database_version: float
    delta: Optional[str]
    last_sync_id: float
    state: Optional[str]
    subscribed_sync_groups: List[str]


class SynchronizedPayload(BaseModel):
    last_sync_id: float


class TeamConnection(BaseModel):
    edges: List["TeamEdge"]
    nodes: List["Team"]
    page_info: "PageInfo"


class TeamCreateInput(BaseModel):
    auto_archive_period: Optional[float]
    auto_close_period: Optional[float]
    auto_close_state_id: Optional[str]
    color: Optional[str]
    cycle_cooldown_time: Optional[int]
    cycle_duration: Optional[int]
    cycle_issue_auto_assign_completed: Optional[bool]
    cycle_issue_auto_assign_started: Optional[bool]
    cycle_lock_to_active: Optional[bool]
    cycle_start_day: Optional[float]
    cycles_enabled: Optional[bool]
    default_issue_estimate: Optional[float]
    default_template_for_members_id: Optional[str]
    default_template_for_non_members_id: Optional[str]
    description: Optional[str]
    group_issue_history: Optional[bool]
    icon: Optional[str]
    id: Optional[str]
    issue_estimation_allow_zero: Optional[bool]
    issue_estimation_extended: Optional[bool]
    issue_estimation_type: Optional[str]
    issue_ordering_no_priority_first: Optional[bool]
    issue_sort_order_default_to_bottom: Optional[bool]
    key: Optional[str]
    marked_as_duplicate_workflow_state_id: Optional[str]
    name: str
    organization_id: Optional[str]
    private: Optional[bool]
    require_priority_to_leave_triage: Optional[bool]
    timezone: Optional[str]
    triage_enabled: Optional[bool]
    upcoming_cycle_count: Optional[float]


class TeamEdge(BaseModel):
    cursor: str
    node: "Team"


class TeamFilter(BaseModel):
    and_: Optional[List["TeamFilter"]]
    created_at: Optional["DateComparator"]
    description: Optional["NullableStringComparator"]
    id: Optional["IDComparator"]
    issues: Optional["IssueCollectionFilter"]
    key: Optional["StringComparator"]
    name: Optional["StringComparator"]
    or_: Optional[List["TeamFilter"]]
    updated_at: Optional["DateComparator"]


class TeamMembership(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    owner: Optional[bool]
    sort_order: float
    team: "Team"
    updated_at: Any
    user: "User"


class TeamMembershipConnection(BaseModel):
    edges: List["TeamMembershipEdge"]
    nodes: List["TeamMembership"]
    page_info: "PageInfo"


class TeamMembershipCreateInput(BaseModel):
    id: Optional[str]
    owner: Optional[bool]
    sort_order: Optional[float]
    team_id: str
    user_id: str


class TeamMembershipEdge(BaseModel):
    cursor: str
    node: "TeamMembership"


class TeamMembershipPayload(BaseModel):
    last_sync_id: float
    success: bool
    team_membership: Optional["TeamMembership"]


class TeamMembershipUpdateInput(BaseModel):
    owner: Optional[bool]
    sort_order: Optional[float]


class TeamNotificationSubscription(Entity, Node, NotificationSubscription):
    archived_at: Any
    created_at: Any
    id: str
    project: Optional["Project"]
    team: "Team"
    type: str
    updated_at: Any
    user: "User"


class TeamPayload(BaseModel):
    last_sync_id: float
    success: bool
    team: Optional["Team"]


class TeamUpdateInput(BaseModel):
    auto_archive_period: Optional[float]
    auto_close_period: Optional[float]
    auto_close_state_id: Optional[str]
    color: Optional[str]
    cycle_cooldown_time: Optional[int]
    cycle_duration: Optional[int]
    cycle_enabled_start_week: Optional[str]
    cycle_issue_auto_assign_completed: Optional[bool]
    cycle_issue_auto_assign_started: Optional[bool]
    cycle_lock_to_active: Optional[bool]
    cycle_start_day: Optional[float]
    cycles_enabled: Optional[bool]
    default_issue_estimate: Optional[float]
    default_issue_state_id: Optional[str]
    default_template_for_members_id: Optional[str]
    default_template_for_non_members_id: Optional[str]
    description: Optional[str]
    draft_workflow_state_id: Optional[str]
    group_issue_history: Optional[bool]
    icon: Optional[str]
    issue_estimation_allow_zero: Optional[bool]
    issue_estimation_extended: Optional[bool]
    issue_estimation_type: Optional[str]
    issue_ordering_no_priority_first: Optional[bool]
    issue_sort_order_default_to_bottom: Optional[bool]
    key: Optional[str]
    marked_as_duplicate_workflow_state_id: Optional[str]
    merge_workflow_state_id: Optional[str]
    name: Optional[str]
    private: Optional[bool]
    require_priority_to_leave_triage: Optional[bool]
    review_workflow_state_id: Optional[str]
    slack_issue_comments: Optional[bool]
    slack_issue_statuses: Optional[bool]
    slack_new_issue: Optional[bool]
    start_workflow_state_id: Optional[str]
    timezone: Optional[str]
    triage_enabled: Optional[bool]
    upcoming_cycle_count: Optional[float]


class Template(BaseModel):
    archived_at: Any
    created_at: Any
    creator: Optional["User"]
    description: Optional[str]
    id: str
    last_updated_by: Optional["User"]
    name: str
    organization: Optional["Organization"]
    team: Optional["Team"]
    template_data: Any
    type: str
    updated_at: Any


class TemplateConnection(BaseModel):
    edges: List["TemplateEdge"]
    nodes: List["Template"]
    page_info: "PageInfo"


class TemplateCreateInput(BaseModel):
    description: Optional[str]
    id: Optional[str]
    name: str
    team_id: Optional[str]
    template_data: Any
    type: str


class TemplateEdge(BaseModel):
    cursor: str
    node: "Template"


class TemplatePayload(BaseModel):
    last_sync_id: float
    success: bool
    template: "Template"


class TemplateUpdateInput(BaseModel):
    description: Optional[str]
    name: Optional[str]
    team_id: Optional[str]
    template_data: Any


class TimelessDateComparator(BaseModel):
    eq: Any
    gt: Any
    gte: Any
    in_: Optional[List[Any]]
    lt: Any
    lte: Any
    neq: Any
    nin: Optional[List[Any]]


class TokenUserAccountAuthInput(BaseModel):
    email: str
    team_ids_to_join: Optional[List[str]]
    timezone: str
    token: str


class UpdateOrganizationInput(BaseModel):
    allowed_auth_services: Optional[List[str]]
    git_branch_format: Optional[str]
    git_linkback_messages_enabled: Optional[bool]
    git_public_linkback_messages_enabled: Optional[bool]
    linear_preview_flags: Any
    logo_url: Optional[str]
    name: Optional[str]
    oauth_app_review: Optional[bool]
    project_update_reminders_day: Optional["Day"]
    project_update_reminders_hour: Optional[float]
    project_updates_reminder_frequency: Optional["ProjectUpdateReminderFrequency"]
    reduced_personal_information: Optional[bool]
    roadmap_enabled: Optional[bool]
    sla_enabled: Optional[bool]
    url_key: Optional[str]


class UpdateUserInput(BaseModel):
    active: Optional[bool]
    admin: Optional[bool]
    avatar_url: Optional[str]
    description: Optional[str]
    disable_reason: Optional[str]
    display_name: Optional[str]
    name: Optional[str]
    status_emoji: Optional[str]
    status_label: Optional[str]
    status_until_at: Any
    timezone: Optional[str]


class UploadFile(BaseModel):
    asset_url: str
    content_type: str
    filename: str
    headers: List["UploadFileHeader"]
    meta_data: Any
    size: int
    upload_url: str


class UploadFileHeader(BaseModel):
    key: str
    value: str


class UploadPayload(BaseModel):
    last_sync_id: float
    success: bool
    upload_file: Optional["UploadFile"]


class UserAccount(BaseModel):
    archived_at: Any
    created_at: Any
    email: str
    id: str
    name: Optional[str]
    service: str
    updated_at: Any
    users: List["User"]


class UserAccountEmailChange(BaseModel):
    archived_at: Any
    canceled_at: Any
    expires_at: Any
    id: str
    new_email: str
    new_email_verified_at: Any
    old_email: str
    old_email_verified_at: Any
    updated_at: Any


class UserAccountExistsPayload(BaseModel):
    success: bool


class UserAdminPayload(BaseModel):
    success: bool


class UserAuthorizedApplication(BaseModel):
    approval_error_code: Optional[str]
    client_id: str
    created_by_linear: bool
    description: Optional[str]
    developer: str
    developer_url: str
    id: str
    image_url: Optional[str]
    is_authorized: bool
    name: str
    webhooks_enabled: bool


class UserCollectionFilter(BaseModel):
    active: Optional["BooleanComparator"]
    admin: Optional["BooleanComparator"]
    and_: Optional[List["UserCollectionFilter"]]
    assigned_issues: Optional["IssueCollectionFilter"]
    created_at: Optional["DateComparator"]
    display_name: Optional["StringComparator"]
    email: Optional["StringComparator"]
    every: Optional["UserFilter"]
    id: Optional["IDComparator"]
    is_me: Optional["BooleanComparator"]
    length: Optional["NumberComparator"]
    name: Optional["StringComparator"]
    or_: Optional[List["UserCollectionFilter"]]
    some: Optional["UserFilter"]
    updated_at: Optional["DateComparator"]


class UserConnection(BaseModel):
    edges: List["UserEdge"]
    nodes: List["User"]
    page_info: "PageInfo"


class UserEdge(BaseModel):
    cursor: str
    node: "User"


class UserFilter(BaseModel):
    active: Optional["BooleanComparator"]
    admin: Optional["BooleanComparator"]
    and_: Optional[List["UserFilter"]]
    assigned_issues: Optional["IssueCollectionFilter"]
    created_at: Optional["DateComparator"]
    display_name: Optional["StringComparator"]
    email: Optional["StringComparator"]
    id: Optional["IDComparator"]
    is_me: Optional["BooleanComparator"]
    name: Optional["StringComparator"]
    or_: Optional[List["UserFilter"]]
    updated_at: Optional["DateComparator"]


class UserFlagType(str, Enum):
    all = "all"
    analyticsWelcomeDismissed = "analyticsWelcomeDismissed"
    canPlaySnake = "canPlaySnake"
    canPlayTetris = "canPlayTetris"
    completedOnboarding = "completedOnboarding"
    cycleWelcomeDismissed = "cycleWelcomeDismissed"
    desktopDownloadToastDismissed = "desktopDownloadToastDismissed"
    desktopInstalled = "desktopInstalled"
    desktopTabsOnboardingDismissed = "desktopTabsOnboardingDismissed"
    dueDateShortcutMigration = "dueDateShortcutMigration"
    emptyActiveIssuesDismissed = "emptyActiveIssuesDismissed"
    emptyBacklogDismissed = "emptyBacklogDismissed"
    emptyCustomViewsDismissed = "emptyCustomViewsDismissed"
    emptyMyIssuesDismissed = "emptyMyIssuesDismissed"
    figmaPromptDismissed = "figmaPromptDismissed"
    importBannerDismissed = "importBannerDismissed"
    insightsHelpDismissed = "insightsHelpDismissed"
    insightsWelcomeDismissed = "insightsWelcomeDismissed"
    issueLabelSuggestionUsed = "issueLabelSuggestionUsed"
    issueMovePromptCompleted = "issueMovePromptCompleted"
    joinTeamIntroductionDismissed = "joinTeamIntroductionDismissed"
    listSelectionTip = "listSelectionTip"
    migrateThemePreference = "migrateThemePreference"
    milestoneOnboardingIsSeenAndDismissed = "milestoneOnboardingIsSeenAndDismissed"
    projectBacklogWelcomeDismissed = "projectBacklogWelcomeDismissed"
    projectUpdatesWelcomeDismissed = "projectUpdatesWelcomeDismissed"
    projectWelcomeDismissed = "projectWelcomeDismissed"
    rewindBannerDismissed = "rewindBannerDismissed"
    slackCommentReactionTipShown = "slackCommentReactionTipShown"
    teamsPageIntroductionDismissed = "teamsPageIntroductionDismissed"
    threadedCommentsNudgeIsSeen = "threadedCommentsNudgeIsSeen"
    triageWelcomeDismissed = "triageWelcomeDismissed"


class UserFlagUpdateOperation(str, Enum):
    clear = "clear"
    decr = "decr"
    incr = "incr"
    lock = "lock"


class UserPayload(BaseModel):
    last_sync_id: float
    success: bool
    user: Optional["User"]


class UserRoleType(str, Enum):
    admin = "admin"
    guest = "guest"
    user = "user"


class UserSettings(BaseModel):
    archived_at: Any
    calendar_hash: Optional[str]
    created_at: Any
    id: str
    notification_preferences: Any
    unsubscribed_from: List[str]
    updated_at: Any
    user: "User"


class UserSettingsFlagPayload(BaseModel):
    flag: str
    last_sync_id: float
    success: bool
    value: int


class UserSettingsFlagsResetPayload(BaseModel):
    last_sync_id: float
    success: bool


class UserSettingsPayload(BaseModel):
    last_sync_id: float
    success: bool
    user_settings: "UserSettings"


class UserSettingsUpdateInput(BaseModel):
    notification_preferences: Any
    settings: Any
    unsubscribed_from: Optional[List[str]]


class ViewPreferences(BaseModel):
    archived_at: Any
    created_at: Any
    id: str
    type: str
    updated_at: Any
    view_type: str


class ViewPreferencesCreateInput(BaseModel):
    custom_view_id: Optional[str]
    cycle_id: Optional[str]
    id: Optional[str]
    label_id: Optional[str]
    preferences: Any
    project_id: Optional[str]
    roadmap_id: Optional[str]
    team_id: Optional[str]
    type: "ViewPreferencesType"
    user_id: Optional[str]
    view_type: "ViewType"


class ViewPreferencesPayload(BaseModel):
    last_sync_id: float
    success: bool
    view_preferences: "ViewPreferences"


class ViewPreferencesType(str, Enum):
    organization = "organization"
    user = "user"


class ViewPreferencesUpdateInput(BaseModel):
    preferences: Any


class ViewType(str, Enum):
    activeIssues = "activeIssues"
    allIssues = "allIssues"
    archive = "archive"
    backlog = "backlog"
    board = "board"
    completedCycle = "completedCycle"
    customRoadmap = "customRoadmap"
    customView = "customView"
    cycle = "cycle"
    inbox = "inbox"
    label = "label"
    myIssues = "myIssues"
    myIssuesActivity = "myIssuesActivity"
    myIssuesCreatedByMe = "myIssuesCreatedByMe"
    myIssuesSubscribedTo = "myIssuesSubscribedTo"
    project = "project"
    projects = "projects"
    projectsAll = "projectsAll"
    projectsBacklog = "projectsBacklog"
    projectsClosed = "projectsClosed"
    roadmap = "roadmap"
    roadmapAll = "roadmapAll"
    roadmapBacklog = "roadmapBacklog"
    roadmapClosed = "roadmapClosed"
    roadmaps = "roadmaps"
    search = "search"
    teams = "teams"
    triage = "triage"
    userProfile = "userProfile"
    userProfileCreatedByUser = "userProfileCreatedByUser"


class Webhook(BaseModel):
    all_public_teams: bool
    archived_at: Any
    created_at: Any
    creator: Optional["User"]
    enabled: bool
    id: str
    label: Optional[str]
    resource_types: List[str]
    secret: Optional[str]
    team: Optional["Team"]
    updated_at: Any
    url: Optional[str]


class WebhookConnection(BaseModel):
    edges: List["WebhookEdge"]
    nodes: List["Webhook"]
    page_info: "PageInfo"


class WebhookCreateInput(BaseModel):
    all_public_teams: Optional[bool]
    enabled: Optional[bool]
    id: Optional[str]
    label: Optional[str]
    resource_types: List[str]
    secret: Optional[str]
    team_id: Optional[str]
    url: str


class WebhookEdge(BaseModel):
    cursor: str
    node: "Webhook"


class WebhookPayload(BaseModel):
    last_sync_id: float
    success: bool
    webhook: "Webhook"


class WebhookUpdateInput(BaseModel):
    enabled: Optional[bool]
    label: Optional[str]
    resource_types: Optional[List[str]]
    secret: Optional[str]
    url: Optional[str]


class WorkflowCondition(BaseModel):
    issue_filter: Optional["IssueFilter"]
    project_filter: Optional["ProjectFilter"]


class WorkflowCronJobDefinition(BaseModel):
    activities: Any
    archived_at: Any
    created_at: Any
    creator: "User"
    description: Optional[str]
    enabled: bool
    id: str
    name: str
    schedule: Any
    sort_order: str
    team: "Team"
    updated_at: Any


class WorkflowCronJobDefinitionConnection(BaseModel):
    edges: List["WorkflowCronJobDefinitionEdge"]
    nodes: List["WorkflowCronJobDefinition"]
    page_info: "PageInfo"


class WorkflowCronJobDefinitionEdge(BaseModel):
    cursor: str
    node: "WorkflowCronJobDefinition"


class WorkflowDefinition(BaseModel):
    activities: Any
    archived_at: Any
    conditions: Any
    created_at: Any
    creator: "User"
    description: Optional[str]
    enabled: bool
    group_name: Optional[str]
    id: str
    name: str
    sort_order: str
    team: Optional["Team"]
    trigger: "WorkflowTrigger"
    trigger_type: "WorkflowTriggerType"
    type: "WorkflowType"
    updated_at: Any


class WorkflowDefinitionConnection(BaseModel):
    edges: List["WorkflowDefinitionEdge"]
    nodes: List["WorkflowDefinition"]
    page_info: "PageInfo"


class WorkflowDefinitionEdge(BaseModel):
    cursor: str
    node: "WorkflowDefinition"


class WorkflowStateConnection(BaseModel):
    edges: List["WorkflowStateEdge"]
    nodes: List["WorkflowState"]
    page_info: "PageInfo"


class WorkflowStateCreateInput(BaseModel):
    color: str
    description: Optional[str]
    id: Optional[str]
    name: str
    position: Optional[float]
    team_id: str
    type: str


class WorkflowStateEdge(BaseModel):
    cursor: str
    node: "WorkflowState"


class WorkflowStateFilter(BaseModel):
    and_: Optional[List["WorkflowStateFilter"]]
    created_at: Optional["DateComparator"]
    description: Optional["StringComparator"]
    id: Optional["IDComparator"]
    issues: Optional["IssueCollectionFilter"]
    name: Optional["StringComparator"]
    or_: Optional[List["WorkflowStateFilter"]]
    position: Optional["NumberComparator"]
    team: Optional["TeamFilter"]
    type: Optional["StringComparator"]
    updated_at: Optional["DateComparator"]


class WorkflowStatePayload(BaseModel):
    last_sync_id: float
    success: bool
    workflow_state: "WorkflowState"


class WorkflowStateUpdateInput(BaseModel):
    color: Optional[str]
    description: Optional[str]
    name: Optional[str]
    position: Optional[float]


class WorkflowTrigger(str, Enum):
    entityCreated = "entityCreated"
    entityCreatedOrUpdated = "entityCreatedOrUpdated"
    entityRemoved = "entityRemoved"
    entityUnarchived = "entityUnarchived"
    entityUpdated = "entityUpdated"


class WorkflowTriggerType(str, Enum):
    issue = "issue"
    project = "project"


class WorkflowType(str, Enum):
    custom = "custom"
    sla = "sla"


class WorkspaceAuthorizedApplication(BaseModel):
    app_id: str
    client_id: str
    image_url: Optional[str]
    memberships: List["AuthMembership"]
    name: str
    scope: List[str]
    total_members: float
    webhooks_enabled: bool


class ZendeskSettings(BaseModel):
    automate_ticket_reopening_on_cancellation: Optional[bool]
    automate_ticket_reopening_on_comment: Optional[bool]
    automate_ticket_reopening_on_completion: Optional[bool]
    bot_user_id: Optional[str]
    send_note_on_comment: Optional[bool]
    send_note_on_status_change: Optional[bool]
    subdomain: str
    url: str


class ZendeskSettingsInput(BaseModel):
    automate_ticket_reopening_on_cancellation: Optional[bool]
    automate_ticket_reopening_on_comment: Optional[bool]
    automate_ticket_reopening_on_completion: Optional[bool]
    bot_user_id: Optional[str]
    send_note_on_comment: Optional[bool]
    send_note_on_status_change: Optional[bool]
    subdomain: str
    url: str


