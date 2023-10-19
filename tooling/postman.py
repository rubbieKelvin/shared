# creates a postman collection from api
import uuid
import typing
import pydantic

from shared.view_tools.paths import Api
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view


class PostmanV2Collection:
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

    class Variable(pydantic.BaseModel):
        key: str
        value: str
        type: typing.Literal["string"] = "string"

    def __init__(self, *, info: Info) -> None:
        self.info = info
        self.variables: list[PostmanV2Collection.Variable] = []

    def add_var(self, key: str, value: str):
        var = PostmanV2Collection.Variable(key=key, value=value)
        self.variables.append(var)

    @property
    def view(self) -> typing.Callable:
        @api_view()
        def postman_v2_collection(r: Request) -> Response:
            info = self.info.model_dump(by_alias=True)
            variable = [v.model_dump() for v in self.variables]

            return Response({"info": info, "variable": variable})

        return postman_v2_collection
