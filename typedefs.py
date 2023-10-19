import typing

# roles essential to the backend functions
InternalRole = typing.Literal["admin", "anonymous", "user"]

Json: typing.TypeAlias = (
    int | str | bool | float | None | list["Json"] | dict[str, "Json"]
)

HTTP_METHODS = typing.Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
