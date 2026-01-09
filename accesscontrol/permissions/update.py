import typing as t

from django.db.models import Q
from pydantic import BaseModel


class UpdatePermissionConfig[T: BaseModel](t.TypedDict):
    mode: t.Literal["UPDATE_ONE_ONLY", "UPDATE_MANY_ONLY", "UPDATE_ONE_AND_MANY"]
    rows: t.NotRequired[Q]
    columns: t.NotRequired[list[str]]
    schema: t.NotRequired[T]
