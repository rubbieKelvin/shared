import typing

Json: typing.TypeAlias = (
    int | str | bool | float | None | list["Json"] | dict[str, "Json"]
)

HTTP_METHODS = typing.Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


class NotSet:
    """Use this class instead of None for propertites and fields that were not set"""

    _instance = None

    def __new__(cls) -> "NotSet":
        if cls._instance == None:
            cls._instance = super(NotSet, cls).__new__(cls)
        return cls._instance

    def __bool__(self):
        return False

    def __repr__(self) -> str:
        return "NotSet"
