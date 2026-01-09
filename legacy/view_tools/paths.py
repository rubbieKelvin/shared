import re
import typing
import functools

from dataclasses import dataclass
from django.urls import path as path_, URLPattern
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import (
    BasePermission,
    OperandHolder,
    AllowAny,
    SingleOperandHolder,
)

from . import exceptions
from shared.typedefs import HTTP_METHODS

PERMISSION_INPUT_TYPES: typing.TypeAlias = (
    type[BasePermission] | OperandHolder | SingleOperandHolder
)


def handle_err(func: typing.Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.ApiException as error:
            message: exceptions.Error = {
                "error": error.message,
                "code": error.code,
            }
            return Response(message, status=error.response_status)
        except Exception as e:
            raise e

    return wrapper


@dataclass
class ApiStruct:
    """
    A data class representing an API endpoint.

    Attributes:
        function (Callable): The view function associated with the endpoint.
        method (HTTP_METHODS): The HTTP method supported by the endpoint.
        path (str): The URL path for the endpoint.
        name (str): The name of the endpoint (optional).
    """

    function: typing.Callable
    path: str
    name: str | None
    api_parent_class: "Api"

    @property
    def full_path(self) -> str:
        url_path = (
            f"{self.api_parent_class.prefix}{self.path}"
            if self.api_parent_class.prefix
            else self.path
        )

        if url_path.endswith("/"):
            return url_path[:-1]

        return url_path


class Api:
    """
    A class for defining API endpoints using Django REST framework decorators.

    Args:
        prefix (str, optional): A prefix to add to all endpoint paths. Must end with a slash if specified.

    Example:
        api = Api(prefix='/api/v1/')

        @api.endpoint(methods=["GET"], path="example/")
        def example_view(request):
            # Your view logic here
    """

    APIs: list["Api"] = []

    # these are the methods that will be handled across this codebase
    USEABLE_METHODS: list[HTTP_METHODS] = ["DELETE", "GET", "PATCH", "POST", "PUT"]

    def __init__(
        self,
        prefix: str | None = None,
        tags: list[str] | None = None,
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        """
        Initialize an Api instance.

        Args:
            prefix (str, optional): A prefix to add to all endpoint paths. Must end with a slash if specified.
            tags (list[str], optional): A list of strings to classify this endpoint
        """
        prefix = prefix.strip() if type(prefix) is str else prefix

        assert (
            prefix == None or type(prefix) == str
        ), "Prefix should be None or string type"
        assert prefix != "", "Prefix cannot be an empty string"
        assert (prefix is None) or prefix.endswith(
            "/"
        ), "Prefix must end with a slash if specified"

        self.prefix = prefix
        self.tags = tags or []
        self.name = name
        self.description = description

        self.endpoints: list[ApiStruct] = []
        Api.APIs.append(self)

    def endpoint(
        self,
        path: str,
        *,
        method: HTTP_METHODS | None = None,
        name: str | None = None,
        permission: PERMISSION_INPUT_TYPES | None = None,
    ):
        """
        Define an API endpoint and associate it with a view function.

        Args:
            method (HTTP_METHODS): The HTTP method supported by the endpoint.
            path (str): The URL path for the endpoint.
            name (str, optional): The name of the endpoint (optional).

        Returns:
            callable: A decorator function for defining the endpoint.

        Example:
            @api.endpoint(method="GET", path="example/")
            def example_view(request):
                # Your view logic here
        """

        assert not path.startswith("/"), "path must not start with a slash"
        method = method or "GET"
        path = path.strip()

        def decorator(func: typing.Callable[..., Response]):
            @functools.wraps(func)
            @api_view([method])
            @permission_classes([permission] if permission else [AllowAny])
            def wrapper(*args, **kwargs) -> Response:
                try:
                    return func(*args, **kwargs)
                except exceptions.ApiException as error:
                    message: exceptions.Error = {
                        "error": error.message,
                        "code": error.code,
                    }
                    return Response(message, status=error.response_status)

            # store the function and properties
            struct = ApiStruct(wrapper, path, name, api_parent_class=self)

            # intance-wide list
            self.endpoints.append(struct)

            return wrapper

        return decorator

    def endpoint_class(
        self,
        path: str,
        *,
        name: str | None = None,
        permission: PERMISSION_INPUT_TYPES | None = None,
    ):
        """Like the endpoint method, but this one is used to wrap a class.
        the class can now handle diffrent http verbs with different methods to allow for flexibility.

        Args:
            path (str): The URL path for the endpoint
            name (str, optional): The name of the endpoint
            permission (type[BasePermission] | OperandHolder | SingleOperandHolder, optional): The permission class that protects this view

        Returns:
            type: An APIView extended class

        Example:
            @api.endpoint_class("test")
            class Test:
                def get(self, request: Request) -> Response:
                    # get logic

                def post(self, request: Request) -> Response:
                    # post logic

                def put(self, request: Request) -> Response:
                    # put logic

                def patch(self, request: Request) -> Response:
                    # patch logic

                def delete(self, request: Request) -> Response:
                    # delete logic
        """

        assert not path.startswith("/"), "path must not start with a slash"
        path = path.strip()

        def decorator(class_: type):
            class ExposedAPIView(APIView, class_):
                __doc__ = class_.__doc__ or f"Api view for {path}"

                permission_classes = [permission] if permission else [AllowAny]

                @handle_err
                def get(self, *args, **kwargs):
                    handler = getattr(super(), "get", self.http_method_not_allowed)
                    return handler(*args, **kwargs)

                @handle_err
                def post(self, *args, **kwargs):
                    handler = getattr(super(), "post", self.http_method_not_allowed)
                    return handler(*args, **kwargs)

                @handle_err
                def patch(self, *args, **kwargs):
                    handler = getattr(super(), "patch", self.http_method_not_allowed)
                    return handler(*args, **kwargs)

                @handle_err
                def delete(self, *args, **kwargs):
                    handler = getattr(super(), "delete", self.http_method_not_allowed)
                    return handler(*args, **kwargs)

                @handle_err
                def put(self, *args, **kwargs):
                    handler = getattr(super(), "put", self.http_method_not_allowed)
                    return handler(*args, **kwargs)

            ExposedAPIView.__name__ = class_.__name__

            struct = ApiStruct(
                ExposedAPIView.as_view(),
                path,
                name or class_.__name__,
                api_parent_class=self,
            )

            # intance-wide list
            self.endpoints.append(struct)

            return ExposedAPIView

        return decorator

    @property
    def paths(self) -> list[URLPattern]:
        """
        Generate URL patterns for all defined API endpoints.

        Returns:
            list of URLPattern: A list of Django URL patterns for the API endpoints.

        Example:
            urlpatterns = [
                path("admin/", admin.site.urls),
                *api.paths,
            ]
        """

        return [
            path_(
                endpoint.full_path,
                endpoint.function,
                name=endpoint.name or endpoint.function.__name__,
            )
            for endpoint in self.endpoints
        ]
