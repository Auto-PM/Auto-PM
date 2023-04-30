from __future__ import annotations

from typing import Any, Optional, List
from pydantic import BaseModel

class IDComparator(BaseModel):
    eq: Optional[str]
    in_: Optional[List[str]]
    neq: Optional[str]
    nin: Optional[List[str]]


class EstimateComparator(BaseModel):
    and_: Optional[List["NullableNumberComparator"]]
    eq: Optional[float]
    gt: Optional[float]
    gte: Optional[float]
    in_: Optional[List[float]]
    lt: Optional[float]
    lte: Optional[float]
    neq: Optional[float]
    nin: Optional[List[float]]
    null: Optional[bool]
    or_: Optional[List["NullableNumberComparator"]]


class ContentComparator(BaseModel):
    contains: Optional[str]
    not_contains: Optional[str]


class BooleanComparator(BaseModel):
    eq: Optional[bool]
    neq: Optional[bool]


class DateComparator(BaseModel):
    eq: Any
    gt: Any
    gte: Any
    in_: Optional[List[Any]]
    lt: Any
    lte: Any
    neq: Any
    nin: Optional[List[Any]]


class NullableCycleFilter(BaseModel):
    and_: Optional[List["NullableCycleFilter"]]
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
    null: Optional[bool]
    number: Optional["NumberComparator"]
    or_: Optional[List["NullableCycleFilter"]]
    starts_at: Optional["DateComparator"]
    team: Optional["TeamFilter"]
    updated_at: Optional["DateComparator"]


class NullableDateComparator(BaseModel):
    eq: Any
    gt: Any
    gte: Any
    in_: Optional[List[Any]]
    lt: Any
    lte: Any
    neq: Any
    nin: Optional[List[Any]]
    null: Optional[bool]


class NullableIssueFilter(BaseModel):
    and_: Optional[List["NullableIssueFilter"]]
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
    null: Optional[bool]
    number: Optional["NumberComparator"]
    or_: Optional[List["NullableIssueFilter"]]
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


class NullableNumberComparator(BaseModel):
    eq: Optional[float]
    gt: Optional[float]
    gte: Optional[float]
    in_: Optional[List[float]]
    lt: Optional[float]
    lte: Optional[float]
    neq: Optional[float]
    nin: Optional[List[float]]
    null: Optional[bool]


class NullableProjectFilter(BaseModel):
    and_: Optional[List["NullableProjectFilter"]]
    created_at: Optional["DateComparator"]
    creator: Optional["UserFilter"]
    id: Optional["IDComparator"]
    issues: Optional["IssueCollectionFilter"]
    lead: Optional["NullableUserFilter"]
    members: Optional["UserFilter"]
    name: Optional["StringComparator"]
    null: Optional[bool]
    or_: Optional[List["NullableProjectFilter"]]
    roadmaps: Optional["RoadmapCollectionFilter"]
    slug_id: Optional["StringComparator"]
    start_date: Optional["NullableDateComparator"]
    state: Optional["StringComparator"]
    target_date: Optional["NullableDateComparator"]
    updated_at: Optional["DateComparator"]


class NullableProjectMilestoneFilter(BaseModel):
    and_: Optional[List["NullableProjectMilestoneFilter"]]
    created_at: Optional["DateComparator"]
    id: Optional["IDComparator"]
    null: Optional[bool]
    or_: Optional[List["NullableProjectMilestoneFilter"]]
    updated_at: Optional["DateComparator"]


class NullableStringComparator(BaseModel):
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
    null: Optional[bool]
    starts_with: Optional[str]


class NullableTimelessDateComparator(BaseModel):
    eq: Any
    gt: Any
    gte: Any
    in_: Optional[List[Any]]
    lt: Any
    lte: Any
    neq: Any
    nin: Optional[List[Any]]
    null: Optional[bool]


class NullableUserFilter(BaseModel):
    active: Optional["BooleanComparator"]
    admin: Optional["BooleanComparator"]
    and_: Optional[List["NullableUserFilter"]]
    assigned_issues: Optional["IssueCollectionFilter"]
    created_at: Optional["DateComparator"]
    display_name: Optional["StringComparator"]
    email: Optional["StringComparator"]
    id: Optional["IDComparator"]
    is_me: Optional["BooleanComparator"]
    name: Optional["StringComparator"]
    null: Optional[bool]
    or_: Optional[List["NullableUserFilter"]]
    updated_at: Optional["DateComparator"]


