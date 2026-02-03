import typing as t

from django.db import models

type ObjectSerializationMode = t.Literal["SERIALIZE_AS_STRING", "SERIALIZE_AS_PK"]
type SerializationStructure = dict[
    str, "t.Literal[True]|ObjectSerializationMode|SerializationStructure"
]


def struct(
    *args: str,
    __related_field_query: models.Q | None = None,
    **nested: SerializationStructure | ObjectSerializationMode,
) -> SerializationStructure:
    """Defines the structure that a model should be represented as in json format."""
    res: SerializationStructure = {
        **{k: True for k in args},
        **nested,
    }

    if __related_field_query is not None:
        res["__related_field_query"] = __related_field_query  # pyright: ignore[reportArgumentType]

    return res
