import typing
import functools

from dataclasses import dataclass
from django.urls import path as path_, URLPattern
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

HTTP_METHODS = typing.Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
PERMISSION_INPUT_TYPES: typing.TypeAlias = (
    type[BasePermission] | OperandHolder | SingleOperandHolder
)


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

    def __init__(self, prefix: str | None = None) -> None:
        """
        Initialize an Api instance.

        Args:
            prefix (str, optional): A prefix to add to all endpoint paths. Must end with a slash if specified.
        """

        assert (prefix is None) or prefix.endswith(
            "/"
        ), "Prefix must end with a slash if specified"

        self.prefix = prefix
        self.endpoints: list[ApiStruct] = []

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
            @api_view([method])
            @permission_classes([permission] if permission else [AllowAny])
            @functools.wraps(func)
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
            struct = ApiStruct(wrapper, path, name)
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

            ExposedAPIView.__name__ = class_.__name__

            struct = ApiStruct(ExposedAPIView.as_view(), path, name)
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
                self._make_url_path(endpoint),
                endpoint.function,
                name=endpoint.name or endpoint.function.__name__,
            )
            for endpoint in self.endpoints
        ]

    def _make_url_path(self, endpoint: ApiStruct):
        url_path = f"{self.prefix}{endpoint.path}" if self.prefix else endpoint.path
        if url_path.endswith("/"):
            return url_path[:-1]
        return url_path
