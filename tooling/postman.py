# creates a postman collection from api
import re
import uuid
import typing
import pydantic

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from shared.view_tools.paths import Api, ApiStruct
from shared.typedefs import HTTP_METHODS


def resolve_django_url_path_to_field_pattern(path_string: str) -> str:
    """
    Resolves Django URL path patterns to Postman field patterns.

    Args:
        path_string (str): The Django URL path pattern.

    Returns:
        str: The corresponding Postman field pattern.
    """

    # Define a regular expression pattern to match "<data_type:name>"
    pattern = r"<(\w+):(\w+)>"

    # Use the re.sub function to replace the matched patterns with just the names
    path_string = re.sub(pattern, r"<\2>", path_string)

    # replace arrow braces
    field_pattern = path_string.replace("<", ":").replace(">", "")

    return field_pattern


def get_djang_url_path_arguments(
    path_string: str,
) -> list[str]:
    """
    Extracts variable names from a Django URL path pattern.

    Args:
        path_string (str): The Django URL path pattern.

    Returns:
        list[str]: A list of variable names found in the pattern.
    """
    # Use re.findall to extract variable names from the path string
    pattern = r"<(?:\w+:)?(\w+)>"
    return re.findall(pattern, path_string)


def as_postman_var(var_name: str) -> str:
    """
    Converts a variable name to a Postman variable format.

    Args:
        var_name (str): The variable name to convert.

    Returns:
        str: The variable name in Postman format (e.g., {{variable_name}}).
    """

    return "{{" + var_name + "}}"


class PostmanV2Collection:
    """
    Generates a Postman collection from Django API endpoints.
    """

    BASE_URL_VAR_NAME = "BASE_URL"

    class Info(pydantic.BaseModel):
        """
        Information about the Postman collection.
        """

        name: str
        description: str | None = None

        # ...
        schema_: str = pydantic.Field(
            alias="schema",
            serialization_alias="schema",
            default="https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        )
        postman_id: uuid.UUID = pydantic.Field(
            default_factory=uuid.uuid4,
            serialization_alias="_postman_id",
        )

    class Folder(pydantic.BaseModel):
        """
        Represents a folder within the Postman collection.
        """

        name: str
        description: str | None
        item: "typing.Sequence[PostmanV2Collection.Endpoint|PostmanV2Collection.Folder]" = pydantic.Field(
            default_factory=list
        )

        @staticmethod
        def from_api(api: Api) -> "PostmanV2Collection.Folder":
            name = api.name or f"api_{uuid.uuid4().__str__()[:8]}"
            description = api.description
            item = [
                PostmanV2Collection.Endpoint.from_api_struct(struct)
                for struct in api.endpoints
            ]

            return PostmanV2Collection.Folder(
                name=name, description=description, item=item
            )

    class Endpoint(pydantic.BaseModel):
        """
        Represents an API endpoint within the Postman collection.
        """

        class EndpointRequest(pydantic.BaseModel):
            class URL(pydantic.BaseModel):
                class Query(pydantic.BaseModel):
                    key: str
                    value: str = "<value>"
                    description: str | None = None

                class Variable(pydantic.BaseModel):
                    key: str
                    value: str = "<value>"

                class Body(pydantic.BaseModel):
                    mode: str = "raw"
                    raw: str | None = None
                    options: dict = pydantic.Field(default_factory=dict)

                raw: str
                host: tuple[str]
                path: list[str]
                body: Body | None = None
                query: list[Query] = pydantic.Field(default_factory=list)
                variable: list[Variable] = pydantic.Field(default_factory=list)

                @staticmethod
                def from_api_struct(
                    struct: ApiStruct,
                ) -> "PostmanV2Collection.Endpoint.EndpointRequest.URL":
                    raw_path = resolve_django_url_path_to_field_pattern(
                        f"{as_postman_var(PostmanV2Collection.BASE_URL_VAR_NAME)}/{struct.full_path}"
                    )
                    return PostmanV2Collection.Endpoint.EndpointRequest.URL(
                        raw=raw_path,
                        host=(as_postman_var(PostmanV2Collection.BASE_URL_VAR_NAME),),
                        path=resolve_django_url_path_to_field_pattern(
                            struct.full_path
                        ).split("/"),
                        variable=[
                            PostmanV2Collection.Endpoint.EndpointRequest.URL.Variable(
                                key=v
                            )
                            for v in get_djang_url_path_arguments(struct.full_path)
                        ],
                    )

            url: URL
            method: HTTP_METHODS
            description: str | None
            header: list = pydantic.Field(default_factory=list)
            body: dict = pydantic.Field(default_factory=dict)

        name: str
        request: EndpointRequest
        response: list = pydantic.Field(default_factory=list)

        @staticmethod
        def from_api_struct(
            struct: ApiStruct,
        ) -> "PostmanV2Collection.Endpoint|PostmanV2Collection.Folder":
            view: APIView | None = getattr(struct.function, "view_class", None)

            if view == None:
                raise ValueError("function should be a rest_framework view")

            description = struct.function.__doc__

            # get acceptable methods that exists on this endpoint
            methods = set([m.lower() for m in Api.USEABLE_METHODS]).intersection(
                view.http_method_names
            )
            methods = list(methods)
            assert len(methods), "Endpoint must handle at least one method"

            if len(methods) == 1:
                return PostmanV2Collection.Endpoint(
                    name=struct.name or struct.function.__name__,
                    request=PostmanV2Collection.Endpoint.EndpointRequest(
                        method=typing.cast(HTTP_METHODS, methods[0].upper()),
                        description=description,
                        url=PostmanV2Collection.Endpoint.EndpointRequest.URL.from_api_struct(
                            struct
                        ),
                    ),
                )

            method_items: list[PostmanV2Collection.Endpoint] = []
            folder_name = struct.name or struct.function.__name__

            for method in methods:
                handler: typing.Callable | None = getattr(view, method, None)

                if not handler:
                    continue

                endpoint = PostmanV2Collection.Endpoint(
                    name=f"{folder_name} {method}",
                    request=PostmanV2Collection.Endpoint.EndpointRequest(
                        method=typing.cast(HTTP_METHODS, method.upper()),
                        description=handler.__doc__,
                        url=PostmanV2Collection.Endpoint.EndpointRequest.URL.from_api_struct(
                            struct
                        ),
                    ),
                )

                method_items.append(endpoint)

            return PostmanV2Collection.Folder(
                name=struct.name or struct.function.__name__,
                description=struct.function.__doc__,
                item=method_items,
            )

    class Variable(pydantic.BaseModel):
        """
        Defines a variable that can be used in the Postman collection.
        """

        key: str
        value: str
        type: typing.Literal["string"] = "string"

    def __init__(self, *, url: str, info: Info) -> None:
        """
        Initializes a Postman collection with a base URL and collection info.

        Args:
            url (str): The base URL of the collection.
            info (Info): Information about the Postman collection.
        """

        self.url = url.strip()
        self.info = info
        self.variables: list[PostmanV2Collection.Variable] = []

        assert not self.url.endswith("/"), "Url should not end with slash"
        self.var(PostmanV2Collection.BASE_URL_VAR_NAME, url)

    def var(self, key: str, value: str):
        """
        Adds a variable to the Postman collection.

        Args:
            key (str): The variable name.
            value (str): The variable value.
        """
        var = PostmanV2Collection.Variable(key=key, value=value)
        self.variables.append(var)

    @property
    def generated_api_schema(self) -> list["PostmanV2Collection.Folder"]:
        """
        Generates the API schema for the Postman collection.

        Returns:
            list[Folder]: A list of folders and endpoints representing the API schema.
        """
        return [PostmanV2Collection.Folder.from_api(api) for api in Api.APIs]

    @property
    def view(self) -> typing.Callable:
        """
        Defines a view function for the Postman collection.

        Returns:
            typing.Callable: The view function for serving the Postman collection.
        """

        @api_view()
        def postman_v2_collection(r: Request) -> Response:
            info = self.info.model_dump(by_alias=True)
            item = [i.model_dump() for i in self.generated_api_schema]
            variable = [v.model_dump() for v in self.variables]

            return Response({"info": info, "item": item, "variable": variable})

        return postman_v2_collection
