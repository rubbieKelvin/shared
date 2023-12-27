from rest_framework.request import Request
from ..exceptions import AccessPermissionError


class PermissionMixin:
    @classmethod
    def permit_get(cls, request: Request):
        raise AccessPermissionError("You're not permitted to access this resource")

    @classmethod
    def permit_insert(cls, request: Request):
        raise AccessPermissionError(
            "You're not permitted to create a resource in this scope"
        )

    @classmethod
    def permit_update(cls, request: Request):
        raise AccessPermissionError("You're not permitted to update a resource")

    @classmethod
    def permit_delete(cls, request: Request):
        raise AccessPermissionError("You're not permitted to delete this resource")
