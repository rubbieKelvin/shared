import typing
from shared.role_utils import internal_role
from dataclasses import dataclass
from rest_framework.request import Request
from shared.typedefs import InternalRole, Json


T = typing.TypeVar("T")
S = typing.TypeVar("S")


@dataclass
class Field(typing.Generic[T, S]):
    # roles that can access this field
    allowed_roles: list[InternalRole | S] | None = None

    # type casting
    cast: typing.Callable[[typing.Any], T] = lambda x: x

    # the default value
    default: typing.Callable[[typing.Any, Request], Json] | None = None

    # where to access this field from in the original
    resolver: typing.Callable[[typing.Any, str], typing.Any] = lambda obj, key: getattr(
        obj, key
    )


@dataclass
class ComputedField(typing.Generic[S]):
    func: typing.Callable[[typing.Any, Request], Json]
    allowed_roles: list[InternalRole | S] | None = None


@dataclass
class SerializerField(typing.Generic[S]):
    name: str
    many: bool = False
    allowed_roles: list[InternalRole | S] | None = None

    # where to access this field from in the original
    resolver: typing.Callable[[typing.Any, str], typing.Any] = lambda obj, key: getattr(
        obj, key
    )


class Serializer(typing.Generic[S]):
    field: type[Field] = Field
    __serializers__: dict[str, "type[Serializer]"] = {}

    def __init__(self, obj: typing.Any, request: Request) -> None:
        """
        Initialize a Serializer instance.

        Args:
            obj (typing.Any): The object to serialize.
            request (Request): The Django Rest Framework request object.

        Returns:
            None

        Example:
            Create a Serializer instance:
            user_serializer = UserSr(user_instance, request_instance)
        """

        self.obj = obj
        self.request = request

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)
        cls.__serializers__[cls.__name__] = cls

    def __call__(self) -> dict[str, Json]:
        """
        Make the Serializer instance callable to obtain the serialized value.

        Returns:
            dict: A dictionary representing the serialized data.

        Example:
            Get the serialized value from a UserSr instance:
            value = user_serializer()
        """

        fields = [
            attr
            for attr in dir(self)
            if isinstance(getattr(self, attr), (Field, ComputedField, SerializerField))
        ]

        result = {}

        for field_name in fields:
            field_obj: Field | ComputedField | SerializerField = getattr(
                self, field_name
            )

            if (
                field_obj.allowed_roles is None
                or internal_role(self.request) in field_obj.allowed_roles
            ):
                if isinstance(field_obj, Field):
                    try:
                        res = field_obj.resolver(self.obj, field_name)
                    except AttributeError:
                        res = None

                        if field_obj.default:
                            res = field_obj.default(self.obj, self.request)

                    result[field_name] = res

                elif isinstance(field_obj, ComputedField):
                    result[field_name] = field_obj.func(self.obj, self.request)

                elif isinstance(field_obj, SerializerField):
                    value = field_obj.resolver(self.obj, field_name)
                    class_ = Serializer.__serializers__[field_obj.name]

                    if field_obj.many:
                        result[field_name] = [
                            class_(item, self.request)() for item in value
                        ]

                    else:
                        serializer = class_(value, self.request)
                        result[field_name] = serializer()

        return result

    @staticmethod
    def computed(allowed_roles: list[InternalRole | S] | None = None):
        """
        Decorator that wraps a method that can be resolved into a value.

        Args:
            allowed_roles (list[InternalRole | S] | None, optional):
                A list of internal roles that are allowed to access the computed field.
                If None, the field is accessible to all internal roles. Defaults to None.

        Returns:
            decorator: A decorator function that wraps a method as a computed field.

        Example:
            Define a computed field with access restricted to 'user' internal role:
            @computed(allowed_roles=['user'])
            def full_name_length(obj: typing.Any, request: Request) -> Json:
                return len(getattr(obj, 'first_name', '') + getattr(obj, 'last_name'))
        """

        def decorator(func: typing.Callable[[typing.Any, Request], Json]):
            return ComputedField(func, allowed_roles)

        return decorator

    @staticmethod
    def extended(
        name: str,
        allowed_roles: list[InternalRole | S] | None = None,
        many: bool = False,
        resolver: typing.Callable[[typing.Any, str], typing.Any] | None = None,
    ):
        return SerializerField(
            name,
            allowed_roles=allowed_roles,
            many=many,
            resolver=resolver if resolver else lambda obj, key: getattr(obj, key),
        )
