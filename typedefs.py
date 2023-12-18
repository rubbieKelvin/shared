import typing
from pydantic_core import core_schema, SchemaSerializer

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

    @classmethod
    def _validate(cls, value: "NotSet"):
        return not value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        _ = source_type
        schema = core_schema.no_info_after_validator_function(
            cls._validate,
            handler(set),
            serialization=core_schema.plain_serializer_function_ser_schema(
                set,
                info_arg=False,
                return_schema=core_schema.set_schema(),
            ),
        )

        # https://github.com/pydantic/pydantic/issues/7779#issuecomment-1775629521
        cls.__pydantic_serializer__ = SchemaSerializer(
            schema
        )  # <-- this is necessary for pydantic-core to serialize
        return schema
