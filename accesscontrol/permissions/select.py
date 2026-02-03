import typing as t

from django.db.models import Q


class SelectPermissionConfig(t.TypedDict):
    mode: t.Literal["SELECT_ONE_ONLY", "SELECT_MANY_ONLY", "SELECT_ONE_AND_MANY"]
    columns: t.NotRequired[list[str] | t.Literal["all"]]
    rows: t.NotRequired[Q]
    allow_aggregation_queries: t.NotRequired[bool]
