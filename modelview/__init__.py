import typing as t

from django.db.models import Model, QuerySet

import typedefs
from accesscontrol.permissions import PermissionSet
from accesscontrol.roles import RoleSet


class ModelView[T: Model]:
    """ModelView describes a model and how it can be accessed."""

    permissions: dict[RoleSet[t.Any], PermissionSet[t.Any, t.Any]] = {}
    model: type[T]  # pyright:ignore[reportUninitializedInstanceVariable]

    def name(self) -> str:
        return self.model._meta.model_name or self.__class__.__name__

    def get(self, _pk: typedefs.Pk) -> T | None:
        raise NotImplementedError

    def find(self) -> QuerySet[T]:
        raise NotImplementedError

    def update(self) -> T:
        raise NotImplementedError

    def delete(self) -> None:
        raise NotImplementedError

    def insert(self) -> T:
        raise NotImplementedError

    @staticmethod
    def view():
        pass
