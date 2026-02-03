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


class FULL_ACCESS:
    insert: InsertPermissionConfig[t.Any] = {"mode": "INSERT_ONE_AND_MANY", "columns": "all"}
    delete: DeletePermissionConfig = {"mode": "DELETE_ONE_AND_MANY", "rows": Q()}
    select: SelectPermissionConfig = {"mode": "SELECT_ONE_AND_MANY", "rows": Q(), "columns": "all"}
    update: UpdatePermissionConfig[t.Any] = {"mode": "UPDATE_ONE_AND_MANY", "columns": "all", "rows": Q()}
