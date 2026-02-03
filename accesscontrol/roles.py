import typing as t

from rest_framework.request import Request

if t.TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


class RoleSet:
    """Classes that limits access to certain resources"""

    __map: dict[str, "RoleSet"] = {}

    def __init__(self, name: str):
        self.name = name
        if name in self.__map:
            raise ValueError(f"Duplicate role: {name}")
        RoleSet.__map[name] = self

    @staticmethod
    def getrole(request: Request) -> "RoleSet":
        """Verifies that a user is a certain role.
        You'd want to override this if you have more roles"""
        user = t.cast("AbstractUser", request.user)

        # for this implementation, let's create these roles if they dont exist
        for i in ["anonymous", "admin", "user"]:
            if i not in RoleSet.__map:
                _ = RoleSet(i)

        if user.is_anonymous:
            return RoleSet.__map["anonymous"]
        if user.is_superuser:
            return RoleSet.__map["admin"]
        return RoleSet.__map["user"]
