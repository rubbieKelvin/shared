import typing
import pydantic

from uuid import uuid4
from django.db import models

from . import utils
from . import serialization
from shared import typedefs


def _handle_dumps_substructure(
    model_instance: "AbstractModel",
    substructure: serialization.SerializationStructure
    | serialization.ObjectSerializationMode,
):
    if substructure == "SERIALIZE_AS_PK":
        return model_instance.pk
    elif substructure == "SERIALIZE_AS_STRING":
        return model_instance.__str__()
    elif type(substructure) is dict:
        return model_instance.dump(substructure)
    else:
        raise Exception("Ivalid structure value for object field")


class AbstractModel(models.Model):
    DEFAULT_SERIALIZATION_STRUCTURE: serialization.SerializationStructure = {}

    id = models.UUIDField(unique=True, default=uuid4, primary_key=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} pk={str(self.pk)}>"

    def dump(
        self, structure: serialization.SerializationStructure | None = None
    ) -> dict[str, typedefs.Json]:
        structure = structure or self.DEFAULT_SERIALIZATION_STRUCTURE

        # the raw result of the data we gather from the fields
        result = {}

        # get a plain list of all the properties we need to fetch
        # remove all meta properties (ones begining with __, they'll be used for configuration)
        fields = [
            property_name
            for property_name in structure.keys()
            if not property_name.startswith("__")
        ]

        # get information on the related model classes the model is related to
        related_fields = utils.getModelRelatedFields(self.__class__)

        for field in fields:
            if field in related_fields:
                # if the field is found in the related_fields, we want to handle it specially
                related_field = related_fields[field]
                extends_abstract_model_class = issubclass(
                    related_field.model, AbstractModel
                )

                if extends_abstract_model_class:
                    if related_field.type == "object":
                        # handle one to one foriegn key
                        related_model_instance = typing.cast(
                            AbstractModel, getattr(self, field)
                        )
                        sub_structure = structure[field]

                        # make sure the sub_structure is not a boolean
                        assert not (
                            type(sub_structure) is bool
                        ), f"{field} should be a ObjectSerializationMode or SerializationStructure"

                        result[field] = _handle_dumps_substructure(
                            related_model_instance, sub_structure
                        )

                    elif related_field.type == "list":
                        # handle related model
                        sub_structure = structure[field]
                        related_manager = typing.cast(
                            "models.manager.RelatedManager", getattr(self, field)
                        )

                        # if query is also included in the structure
                        query = typing.cast(
                            models.Q | None, structure["__related_field_query"]
                        )

                        # use the query object to filter data if it exists in the structure
                        query_set: models.QuerySet[AbstractModel] = (
                            related_manager.filter(query)
                            if query
                            else related_manager.all()
                        )

                        # make sure the sub_structure is not a boolean
                        assert not (
                            type(sub_structure) is bool
                        ), f"{field} should be a ObjectSerializationMode or SerializationStructure"

                        result[field] = []

                        for item in query_set:
                            result[field].append(
                                _handle_dumps_substructure(item, sub_structure)
                            )

                    else:
                        raise Exception("This part of the code should not be reachable")
            else:
                result[field] = getattr(self, field)

        dynamic_model_config = {k: (typing.Any, v) for k, v in result.items()}
        dynamic_model = pydantic.create_model(
            f"{self.__class__.__name__}_PydanticModel",
            __config__=pydantic.ConfigDict(from_attributes=True),
            __base__=None,
            __module__=__name__,
            __validators__=None,
            __cls_kwargs__=None,
            **dynamic_model_config,
        )

        dumped_data = dynamic_model().model_dump(mode="json")
        return dumped_data
