import typing
from rest_framework import status


class Error(typing.TypedDict):
    error: str
    code: typing.NotRequired[str | None]
    meta: typing.NotRequired[dict | list | None]


class ApiException(BaseException):
    response_status: int = status.HTTP_400_BAD_REQUEST
    default_code: str | None = None

    def __init__(self, msg: str, *args, code: str | None = None) -> None:
        super().__init__(msg, *args)
        self.message = msg
        self.code = code or self.default_code


class ResourceNotFound(ApiException):
    response_status = status.HTTP_404_NOT_FOUND
    default_code = "Resource not found"


class AccessPermissionError(ApiException):
    response_status = status.HTTP_401_UNAUTHORIZED
    default_code = "Access denied"


class Forbidden(ApiException):
    response_status = status.HTTP_403_FORBIDDEN
    default_code = "You are not authorized to access this resource"
