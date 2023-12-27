from typing import Any
from pydantic import BaseModel


class GetOneSchema(BaseModel):
    pk: int | str


class FindManySchema(BaseModel):
    where: dict[str, Any]
    limit: int = 100
    offset: int = 0


class InsertManySchema[T: BaseModel](BaseModel):
    objects: list[T]


class UpdateOneSchema[T: BaseModel](BaseModel):
    pk: int | str
    set_: T


class UpdateManySchema[T: BaseModel](BaseModel):
    pks: list[int | str]
    set_: T
