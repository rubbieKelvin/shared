from typing import Any
from pydantic import BaseModel


class PkSchema(BaseModel):
    pk: int | str


class PksSchema(BaseModel):
    pks: list[int | str]


class FindManySchema(BaseModel):
    where: dict[str, Any]
    limit: int = 100
    offset: int = 0


class InsertManySchema[T: BaseModel](BaseModel):
    objects: list[T]


class UpdateOneSchema[T: BaseModel](PkSchema):
    set_: T


class UpdateManySchema[T: BaseModel](PksSchema):
    set_: T
