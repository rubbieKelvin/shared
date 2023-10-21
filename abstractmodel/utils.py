import typing
import pydantic

from django.db import models
from django.db.models.fields import reverse_related


class RelatedModelInfo(pydantic.BaseModel):
    model: type[models.Model]
    type: typing.Literal["object", "list"]


def getModelRelatedFields(
    modelClass: type[models.Model],
) -> dict[str, RelatedModelInfo]:
    foreign_keys: dict[str, RelatedModelInfo] = {}
    for field in modelClass._meta.get_fields(include_hidden=False):
        if isinstance(field, models.ForeignKey) or isinstance(
            field, reverse_related.ForeignObjectRel
        ):
            foreign_keys[field.name] = RelatedModelInfo(
                model=field.related_model,
                type="object" if field.many_to_one else "list",
            )
    return foreign_keys


def getAllModelFields(
    modelClass: type[models.Model], include_foriegn_keys=True
) -> list[str]:
    """
    Retrieves a list of field names for the specified Django model class.

    This function returns a list of field names for the model class, including both regular fields and foreign key fields. It excludes hidden fields and fields that do not have a related_name attribute.

    Args:
    modelClass (type[models.Model]): a Django model class
    include_foriegn_key (boolean) defaults to true. specifies that foriegn keys should be included in the result

    Returns:
    list[str]: a list of field names for the model"""

    return [
        field.name
        for field in modelClass._meta.get_fields(include_hidden=False)
        if isinstance(field, models.Field)
        or (
            isinstance(field, models.ForeignKey)
            and getattr(field, "related_name", None)
            and include_foriegn_keys
        )
    ]
