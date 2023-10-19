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
from .schema import ApiSchema
from shared.typedefs import HTTP_METHODS

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

    # TODO: remove
    @staticmethod
    def resolve_django_path_to_field_pattern(path_string: str) -> str:
        # Define a regular expression pattern to match "<data_type:name>"
        pattern = r"<(\w+):(\w+)>"

        # Use the re.sub function to replace the matched patterns with just the names
        path_string = re.sub(pattern, r"<\2>", path_string)

        # replace arrow braces
        field_pattern = path_string.replace("<", "{").replace(">", "}")

        return field_pattern

    # TODO: remove
    @staticmethod
    def get_path_arguments(
        path_string: str,
    ) -> list[ApiSchema.PathItem.Operation.Parameter]:
        # Use re.findall to extract variable names from the path string
        pattern = r"<(?:\w+:)?(\w+)>"
        variable_names = re.findall(pattern, path_string)

        return [
            ApiSchema.PathItem.Operation.Parameter(name=var, required=True, in_="path")
            for var in variable_names
        ]

    # TODO: remove
    def get_operation(
        self,
        view: APIView,
        method: typing.Literal[
            "get",
            "put",
            "post",
            "delete",
            "patch",
        ],
    ) -> ApiSchema.PathItem.Operation | None:
        func: typing.Callable | None = getattr(view, method, None)

        if not func:
            return None

        summary = func.__doc__
        tags = self.api_parent_class.tags
        oparationId = f"{self.name or self.function.__name__}:{method}"

        return ApiSchema.PathItem.Operation(
            summary=summary,
            oparationId=oparationId,
            tags=tags,
            parameters=self.get_path_arguments(self.path),
        )

    # TODO: remove
    def generate_schema(self) -> tuple[str, ApiSchema.PathItem]:
        view_class: APIView | None = getattr(self.function, "view_class", None)

        if view_class == None:
            raise ValueError("function should be a rest_framework view")

        field_pattern = self.resolve_django_path_to_field_pattern(self.path)
        description = self.function.__doc__

        get_operation = self.get_operation(view_class, "get")
        put_operation = self.get_operation(view_class, "put")
        post_oparation = self.get_operation(view_class, "post")
        delete_oparation = self.get_operation(view_class, "delete")
        patch_oparation = self.get_operation(view_class, "patch")

        return field_pattern, ApiSchema.PathItem(
            description=description,
            get=get_operation,
            post=post_oparation,
            delete=delete_oparation,
            patch=patch_oparation,
            put=put_operation,
        )


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

    SCHEMA: ApiSchema | None = None
    APIs: list["Api"] = []

    # TODO: remove
    ENDPOINTS: list[ApiStruct] = []

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

            # type-wide list
            Api.ENDPOINTS.append(struct)

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

            struct = ApiStruct(
                ExposedAPIView.as_view(),
                path,
                name or class_.__name__,
                api_parent_class=self,
            )

            # intance-wide list
            self.endpoints.append(struct)

            # type-wide list
            Api.ENDPOINTS.append(struct)

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

    # TODO: remove
    @staticmethod
    def schema(path="openapi/") -> URLPattern:
        # TODO: this handler should be cached
        @api_view()
        def schema_root(_: Request) -> Response:
            if Api.SCHEMA:
                if not Api.SCHEMA.paths:
                    for endpoint in Api.ENDPOINTS:
                        k, v = endpoint.generate_schema()
                        Api.SCHEMA.paths[k] = v

                return Response(Api.SCHEMA.model_dump(by_alias=True))
            return Response({"error": "No schema provided"}, status=404)

        return path_(path, schema_root, name="openapi-schema")
