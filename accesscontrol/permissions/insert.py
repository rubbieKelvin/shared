import typing as t

from pydantic import BaseModel


class InsertPermissionConfig[T: BaseModel](t.TypedDict):
    mode: t.Literal["INSERT_ONE_ONLY", "INSERT_MANY_ONLY", "INSERT_ONE_AND_MANY"]
    columns: t.NotRequired[list[str]]
    schema: t.NotRequired[BaseModel]
