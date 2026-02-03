import typing as t

from django.http import HttpRequest
from django.db.models import Model, Q, QuerySet
from pydantic import BaseModel
from rest_framework.permissions import (
    BasePermission,
    OperandHolder,
    SingleOperandHolder,
)

import exceptions
import typedefs
from accesscontrol.permissions import PermissionSet
from accesscontrol.permissions.delete import DeletePermissionConfig
from accesscontrol.permissions.insert import InsertPermissionConfig
from accesscontrol.permissions.select import SelectPermissionConfig
from accesscontrol.permissions.update import UpdatePermissionConfig
from accesscontrol.roles import RoleSet
from ninja import Router, Path

from .pagination import Pagination, paginate

type Request = HttpRequest
type DjrfPermission = type[BasePermission] | OperandHolder | SingleOperandHolder


class ModelRouter[R: str]:
    type Self = "ModelRouter[R]"

    def __init__(self, model: type[Model]) -> None:
        self.model = model
        self.permission: dict[R, PermissionSet[t.Any, t.Any]] = {}
        self.queryset: Q | None = None
        self.role_factory: t.Callable[[Request], R] | None = None

    def with_queryset(self, qs: Q) -> "Self":
        self.queryset = qs
        return self

    def with_role_factory(self, factory: t.Callable[[Request], R]) -> Self:
        self.role_factory = factory
        return self

    def _get_role(self, request: Request) -> R | None:
        if self.role_factory:
            return self.role_factory(request)
        return None

    def set_insert_permission[B: BaseModel](
        self, permissions: dict[R, InsertPermissionConfig[B]]
    ) -> "Self":
        for role, config in permissions.items():
            _ = self.permission.setdefault(role, {})
            self.permission[role]["insert"] = config
        return self

    def set_update_permission[B: BaseModel](
        self, permissions: dict[R, UpdatePermissionConfig[B]]
    ) -> "Self":
        for role, config in permissions.items():
            _ = self.permission.setdefault(role, {})
            self.permission[role]["update"] = config
        return self

    def set_select_permission[B: BaseModel](
        self, permissions: dict[R, SelectPermissionConfig]
    ) -> "Self":
        for role, config in permissions.items():
            _ = self.permission.setdefault(role, {})
            self.permission[role]["select"] = config
        return self

    def set_delete_permission[B: BaseModel](
        self, permissions: dict[R, DeletePermissionConfig]
    ) -> "Self":
        for role, config in permissions.items():
            _ = self.permission.setdefault(role, {})
            self.permission[role]["delete"] = config
        return self

    def name(self) -> str:
        return self.model._meta.model_name or self.__class__.__name__

    def _request_aware_select_queryset(
        self, request: Request, queryset: QuerySet[t.Any]
    ) -> QuerySet[t.Any]:
        """Use the role to get queryset from permissions that should be applied to row selections"""
        role = self._get_role(request)
        if not role:
            return queryset.none()

        select_config = self.permission[role].get("select", None)

        if not select_config:
            return queryset.none()

        query = select_config.get("rows")
        return queryset.filter(query) if query else queryset

    def _get(self, request: Request, pk: typedefs.Pk) -> Model | None:
        queryset = self._request_aware_select_queryset(
            request,
            self.model.objects.filter(self.queryset)
            if self.queryset
            else self.model.objects.all(),
        )

        try:
            instance = queryset.get(pk=pk)
        except self.model.DoesNotExist:
            return None
        return instance

    def build(self):
        router = Router()
        root = f"model/{self.name()}"

        @router.get(root+"/{pk}")
        def get(self, request: Request, pk: Path[typedefs.Pk]):
            return self._get(request, pk)

        return router
    
