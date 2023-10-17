from shared.view_tools.schema import ApiSchema
from pydantic import AnyUrl

schema = ApiSchema(
    info=ApiSchema.Info(title="My Api", summary="An api built for us"),
    servers=[
        ApiSchema.Server(
            url=AnyUrl("http://localhost:8080/"), description="Local server"
        )
    ],
)


def test_schema_properties():
    assert schema.info.title == "My Api"
    assert schema.info.version == "0.0.0"
    assert schema.openapi == "3.1"


def test_schema_urls():
    server = schema.servers[0]
    assert str(server.url) == "http://localhost:8080/"
