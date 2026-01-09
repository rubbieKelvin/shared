import typing as t

from django.db.models import Model

from accesscontrol.permissions import PermissionSet
from accesscontrol.roles import RoleSet


class ModelView:
    """ModelView describes a model and how it can be accessed."""

    permissions: dict[RoleSet[t.Any], PermissionSet[t.Any, t.Any]] = {}
    model: type[Model] | None = None

    def get(self):
        raise NotImplementedError

    def find(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def insert(self):
        raise NotImplementedError

    @staticmethod
    def view():
        pass
