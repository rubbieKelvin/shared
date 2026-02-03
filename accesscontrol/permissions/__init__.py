import typing as t

from django.db.models import Q
from pydantic import BaseModel

from .delete import DeletePermissionConfig
from .insert import InsertPermissionConfig
from .select import SelectPermissionConfig
from .update import UpdatePermissionConfig


class PermissionSet[InsertSchema: BaseModel, UpdateSchema: BaseModel](t.TypedDict):
    insert: t.NotRequired[InsertPermissionConfig[InsertSchema]]
    select: t.NotRequired[SelectPermissionConfig]
    update: t.NotRequired[UpdatePermissionConfig[UpdateSchema]]
    delete: t.NotRequired[DeletePermissionConfig]


FULL_ACCESS: PermissionSet[t.Any, t.Any] = {
    "insert": {"mode": "INSERT_ONE_AND_MANY", "columns": "all"},
    "delete": {"mode": "DELETE_ONE_AND_MANY", "rows": Q()},
    "select": {"mode": "SELECT_ONE_AND_MANY", "rows": Q(), "columns": "all"},
    "update": {"mode": "UPDATE_ONE_AND_MANY", "columns": "all", "rows": Q()},
}
