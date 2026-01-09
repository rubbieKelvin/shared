import typing as t

from rest_framework import status


class ErrorType(t.TypedDict):
    error: str
    code: t.NotRequired[str | None]
    meta: t.NotRequired[dict[str, t.Any] | list[t.Any]]


class ApiException(BaseException):
    def __init__(
        self,
        msg: str,
        *args: t.Any,
        code: str | None = None,
        status: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(msg, *args)
        self.code = code
        self.message = msg
        self.status = status
