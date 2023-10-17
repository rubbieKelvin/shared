import pydantic


class ApiSchema(pydantic.BaseModel):
    """
    OpenAPI schema based on specifications written; https://swagger.io/specification/
    """

    class Info(pydantic.BaseModel):
        class Contact(pydantic.BaseModel):
            name: str
            email: pydantic.EmailStr
            url: pydantic.AnyUrl | None = None

        class License(pydantic.BaseModel):
            name: str
            url: pydantic.AnyUrl | None = None

        title: str
        summary: str
        description: str | None = None
        contact: Contact | None = None
        termsOfService: pydantic.AnyUrl | None = None
        license: License | None = None
        version: str = "0.0.0"

    class Server(pydantic.BaseModel):
        url: pydantic.AnyUrl
        description: str

    class Tag(pydantic.BaseModel):
        pass

    class ExternalDoc(pydantic.BaseModel):
        pass

    openapi: str = "3.1"
    info: Info
    servers: list[Server] = pydantic.Field(default_factory=list)
    paths: dict = pydantic.Field(default_factory=dict)
    tags: list[Tag] = pydantic.Field(default_factory=list)
    externalDocs: ExternalDoc | None = pydantic.Field(default=None)
