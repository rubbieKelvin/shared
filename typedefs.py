import typing

Json: typing.TypeAlias = (
    int | str | bool | float | None | list["Json"] | dict[str, "Json"]
)

HTTP_METHODS = typing.Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
