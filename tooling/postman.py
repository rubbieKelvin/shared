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
    # Use re.findall to extract variable names from the path string
    pattern = r"<(?:\w+:)?(\w+)>"
    return re.findall(pattern, path_string)


def as_postman_var(var_name: str) -> str:
    return "{{" + var_name + "}}"


class PostmanV2Collection:
    BASE_URL_VAR_NAME = "BASE_URL"

    class Info(pydantic.BaseModel):
        name: str
        description: str | None = None

        # ...
        schema: str = pydantic.Field(
            default="https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        )
        postman_id: uuid.UUID = pydantic.Field(
            default_factory=uuid.uuid4,
            serialization_alias="_postman_id",
        )

    class Folder(pydantic.BaseModel):
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
        class EndpointRequest(pydantic.BaseModel):
            class URL(pydantic.BaseModel):
                class Query(pydantic.BaseModel):
                    key: str
                    value: str = "<value>"
                    description: str | None = None

                class Variable(pydantic.BaseModel):
                    key: str
                    value: str = "<value>"

                raw: str
                host: tuple[str]
                path: list[str]
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
        key: str
        value: str
        type: typing.Literal["string"] = "string"

    def __init__(self, *, url: str, info: Info) -> None:
        self.url = url.strip()
        self.info = info
        self.variables: list[PostmanV2Collection.Variable] = []

        assert not self.url.endswith("/"), "Url should not end with slash"
        self.var(PostmanV2Collection.BASE_URL_VAR_NAME, url)

    def var(self, key: str, value: str):
        var = PostmanV2Collection.Variable(key=key, value=value)
        self.variables.append(var)

    @property
    def generated_api_schema(self) -> list["PostmanV2Collection.Folder"]:
        return [PostmanV2Collection.Folder.from_api(api) for api in Api.APIs]

    @property
    def view(self) -> typing.Callable:
        @api_view()
        def postman_v2_collection(r: Request) -> Response:
            info = self.info.model_dump(by_alias=True)
            item = [i.model_dump() for i in self.generated_api_schema]
            variable = [v.model_dump() for v in self.variables]

            return Response({"info": info, "item": item, "variable": variable})

        return postman_v2_collection
