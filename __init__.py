import typing
from .types import InternalRole
from rest_framework.request import Request
from django.contrib.auth.models import AbstractUser

S = typing.TypeVar("S")


def internal_role(request: Request) -> list[InternalRole | S]:
    """
    Determine the internal role of a user based on their attributes and authentication status.

    Args:
        request: The Django Rest Framework request object containing user information.

    Returns:
        InternalRole: A string indicating the internal role ("admin," "anonymous," or "user").

    Example:
        Determine the internal role of a user by calling internal_role(request).
        Returns "admin" if the user is a staff member or superuser.
        Returns "anonymous" if the user is not authenticated.
        Returns "user" for regular authenticated users.
    """

    user = typing.cast(AbstractUser, request.user)
    roles: list[InternalRole] = []

    if user.is_anonymous:
        return ["anonymous"]

    if user.is_staff or user.is_superuser:
        roles.append("admin")

    # service roles are injected into the request object by the service
    service_roles = typing.cast(list[S], getattr(request, "service_roles", []))

    return ["user", *roles, *service_roles]
