import typing
from pydantic import BaseModel
from django.conf import settings


class AuthConf(BaseModel):
    class Field(BaseModel):
        input_type: typing.Literal["email", "password", "text"]
        placeholder: str
        name: str

    company_name: str | None = None
    application_name: str
    application_url: str
    application_icon_url: str
    callback_url: str
    login_fields: list[Field] = [
        Field(input_type="email", placeholder="Email address", name="email"),
        Field(input_type="password", placeholder="Password", name="password"),
    ]

    @staticmethod
    def from_settings() -> "AuthConf":
        shared_settings = getattr(settings, "SHARED", {})
        try:
            config = shared_settings["AUTHENTICATION_CONFIG"]
        except KeyError:
            raise Exception(
                'Include "AUTHENTICATION_CONFIG" in "SHARED" in your settings'
            )

        assert type(config) == AuthConf
        return config
