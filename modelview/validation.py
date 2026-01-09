import functools
import json
import typing as t

from django.http import QueryDict
from pydantic import BaseModel
from pydantic_core import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


def _get_request_object_from_args(*args: t.Any) -> Request:
    for arg in args:
        if type(arg) is Request:
            return arg
    raise TypeError("Request object is not included in args")


def validate(schema: type[BaseModel]):
    """
    A decorator for validating request data against a Pydantic schema.

    Args:
        schema (type[BaseModel]): The Pydantic schema to validate the request data against.

    Returns:
        callable: A decorator function that can be used to validate request data.

    Usage:
        @validate(MyPydanticSchema)
        def my_view(request):
            # Your view logic here
    """

    def decorator(func: t.Callable[..., Response]):
        @functools.wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> Response:
            request = _get_request_object_from_args([*args, *kwargs.values()])

            try:
                validate_request(schema, t.cast(Request, request))
                return func(*args, **kwargs)

            except ValidationError as error:
                message: exceptions.Error = {
                    "error": "invalid data in body",
                    "code": "INPUT_ERROR",
                    "meta": json.loads(error.json()),
                }

                return Response(
                    message,
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return wrapper

    return decorator


def validate_request[T: BaseModel](schema: type[T], request: Request) -> T:
    data = t.cast(dict[str, t.Any] | QueryDict, request.data)

    if type(data) is QueryDict:
        data = t.cast(dict[str, t.Any], data.dict())

    data = t.cast(dict[str, t.Any], data)
    assert type(data) is dict, "Can only validate map-like request-bodies"

    try:
        model_instance = schema.model_validate(data)
        setattr(request, "validated_body", model_instance)
        return model_instance

    except ValidationError as error:
        raise error


def get_validated_body[M: BaseModel](request: Request) -> M:  # pyright: ignore[reportInvalidTypeVarUse]
    """
    Get the validated request body from a Django Rest Framework request.

    Args:
        request (Request): The Django Rest Framework request object.

    Returns:
        BaseModel: The Pydantic BaseModel instance representing the validated request body.

    Raises:
        AttributeError: If the request has not been wrapped with the @validate decorator,
        and the 'validated_body' attribute has not been set.

    Usage:
        try:
            validated_data = validated_body(request)
        except AttributeError:
            # Handle the case where 'validated_body' attribute is not available.
    """

    instance = getattr(request, "validated_body")
    return t.cast(M, instance)
