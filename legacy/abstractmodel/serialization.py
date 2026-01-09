import typing
from django.db import models

ObjectSerializationMode = typing.Literal["SERIALIZE_AS_STRING", "SERIALIZE_AS_PK"]
SerializationStructure: typing.TypeAlias = dict[
    str, "typing.Literal[True]|ObjectSerializationMode|SerializationStructure"
]


def struct(
    *args: str,
    __related_field_query: models.Q | None = None,
    **kwargs: SerializationStructure | ObjectSerializationMode
) -> SerializationStructure:
    """Defines the structure that a model should be represented as in json format."""
    return {
        **{k: True for k in args},
        **kwargs,
        "__related_field_query": __related_field_query,  # type: ignore
    }
