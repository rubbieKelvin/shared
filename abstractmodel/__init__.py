import typing
import pydantic

from uuid import uuid4
from django.db import models
from django.db.models.fields.related import ForeignKey

from . import utils
from . import serialization
from shared import typedefs


def _handle_dumps_substructure(
    model_instance: models.Model,
    substructure: serialization.SerializationStructure
    | serialization.ObjectSerializationMode,
):
    """
    Handle the serialization of a substructure of an AbstractModel instance.

    This function is responsible for handling the serialization of a substructure
    of an AbstractModel instance. It allows customizing the serialization process
    based on the provided substructure, which can specify how to serialize a related
    model or object field.

    Args:
        model_instance (AbstractModel): The AbstractModel instance to be serialized.
        substructure (serialization.SerializationStructure | serialization.ObjectSerializationMode):
            The substructure that defines how the serialization should be handled.
            It can be either a custom structure or one of the predefined modes:
            - "SERIALIZE_AS_PK": Serialize the related model as its primary key.
            - "SERIALIZE_AS_STRING": Serialize the related model as its string representation.

    Returns:
        typedefs.Json: The serialized data based on the provided substructure.

    Raises:
        Exception: If an invalid structure value is provided for the object field.
    """

    if substructure == "SERIALIZE_AS_PK":
        return model_instance.pk
    elif substructure == "SERIALIZE_AS_STRING":
        return model_instance.__str__()
    elif type(substructure) is dict:
        if isinstance(model_instance, AbstractModel):
            return model_instance.serialize(substructure)
        elif isinstance(model_instance, models.Model):
            return AbstractModel._serialize_regular_model(model_instance)
        else:
            raise Exception("this part of the code should not be reachable")
    else:
        raise Exception("Ivalid structure value for object field")


class AbstractModel(models.Model):
    """
    Abstract base model for all database models in your application. It includes common fields such as 'id',
    'date_created', and 'date_updated'.

    Attributes:
    - id (UUIDField): A unique identifier for the model instance.
    - date_created (DateTimeField): The date and time when the instance was created.
    - date_updated (DateTimeField): The date and time when the instance was last updated.

    This class is designed to be extended by your application's specific models.

    Usage:
    class YourModel(AbstractModel):
        # Your model fields and methods here
    """

    id = models.UUIDField(unique=True, default=uuid4, primary_key=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """
        Return a string representation of the model instance.

        Returns:
            str: A string containing the model's class name and primary key.
        """
        return f"<{self.__class__.__name__} pk={str(self.pk)}>"

    @property
    def default_serialization_structure(self) -> serialization.SerializationStructure:
        """
        Property that generates a default serialization structure for the model based on its fields.

        Returns:
        - serialization.SerializationStructure: The default serialization structure.

        This property should be overridden in concrete model classes to define specific serialization structures
        for the model.

        Example:
        class YourModel(AbstractModel):
            name = models.CharField(max_length=100)
            description = models.TextField()

            @property
            def default_serialization_structure(self):
                return {
                    'name': True,
                    'description': True,
                }

            # or using serialization.struct

            @property
            def default_serialization_structure(self):
                return serialization.struct(
                    'name',
                    'description'
                )

        """
        return serialization.struct(*utils.getAllModelFields(self.__class__))

    @staticmethod
    def _serialize_regular_model(model_instance: models.Model) -> dict:
        """
        Serialize a regular Django model instance into a dictionary.

        This method serializes a regular Django model instance into a dictionary,
        extracting attributes specified by the model's fields. It is used to serialize
        related objects that are not derived from the `AbstractModel` class.

        Args:
            model_instance (models.Model): The regular Django model instance to be serialized.

        Returns:
            dict: A dictionary containing the serialized data for the model instance.

        """
        res = {}
        fields = utils.getAllModelFields(model_instance.__class__)
        for field in fields:
            value = getattr(model_instance, field)

            if isinstance(value, models.Model):
                value = value.pk

            res[field] = value
        return res

    def serialize(
        self, structure: serialization.SerializationStructure | None = None
    ) -> dict[str, typedefs.Json]:
        """
        Serialize the model instance based on the provided structure.

        This method serializes the model instance by extracting specified attributes
        according to the provided serialization structure. The structure can be
        customized for individual model instances.

        Args:
            structure (serialization.SerializationStructure | None, optional):
                A custom serialization structure that specifies which attributes to include
                in the serialized data. If not provided, the default structure specified in
                `default_serialization_structure` will be used.

        Returns:
            dict[str, typedefs.Json]: A dictionary containing the serialized data.

        """

        # Use the provided structure or the default serialization structure
        structure = structure or self.default_serialization_structure

        # Initialize the result dictionary to store serialized data
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
                sub_structure = structure[field]

                # make sure the sub_structure is not a boolean
                sub_structure = serialization.struct(
                    *utils.getAllModelFields(related_field.model)
                    if type(sub_structure) == bool
                    else sub_structure
                )

                if related_field.type == "object":
                    # handle one to one foriegn key
                    related_model_instance = typing.cast(
                        models.Model, getattr(self, field)
                    )

                    result[field] = _handle_dumps_substructure(
                        related_model_instance, sub_structure
                    )

                elif related_field.type == "list":
                    # handle related model
                    related_manager = typing.cast(
                        "models.manager.RelatedManager", getattr(self, field)
                    )

                    # if query is also included in the structure
                    query = typing.cast(
                        models.Q | None, structure["__related_field_query"]
                    )

                    # use the query object to filter data if it exists in the structure
                    query_set: models.QuerySet[models.Model] = (
                        related_manager.filter(query)
                        if query
                        else related_manager.all()
                    )

                    result[field] = []

                    for item in query_set:
                        result[field].append(
                            _handle_dumps_substructure(item, sub_structure)
                        )

                else:
                    raise Exception("This part of the code should not be reachable")
            else:
                # Handle regular fields
                result[field] = getattr(self, field)

        # Create a dynamic Pydantic model to convert the result into a json serializable dictionary
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

        # Serialize the data using the dynamic model
        dumped_data = dynamic_model().model_dump(mode="json")
        return dumped_data
