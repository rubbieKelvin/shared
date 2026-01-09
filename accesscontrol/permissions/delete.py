import typing as t

from django.db.models import Q


class DeletePermissionConfig(t.TypedDict):
    mode: t.Literal["DELETE_ONE_ONLY", "DELETE_MANY_ONLY", "DELETE_ONE_AND_MANY"]
    rows: t.NotRequired[Q]
