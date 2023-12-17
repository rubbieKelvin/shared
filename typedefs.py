import typing

Json: typing.TypeAlias = (
    int | str | bool | float | None | list["Json"] | dict[str, "Json"]
)

HTTP_METHODS = typing.Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


class NotSet:
    """Use this class instead of None for propertites and fields that were not set"""

    pass
