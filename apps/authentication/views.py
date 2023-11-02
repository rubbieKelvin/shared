from pydantic import BaseModel
from django.conf import settings
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


class AuthenticationConfiguration(BaseModel):
    application_name: str
    application_url: str

    @staticmethod
    def from_settings() -> "AuthenticationConfiguration":
        default = dict(
            application_name="RKShared",
            application_url="https://github.com/rubbiekelvin",
        )
        config = getattr(settings, "RK_SHARED_AUTHENTICATION_CONFIG", None) or {}
        return AuthenticationConfiguration.model_validate({**config, **default})


def signup_page(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "authentication/signup.html",
    )


def login_page(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "authentication/login.html",
        {"config": AuthenticationConfiguration.from_settings()},
    )


def logout_page(request: HttpRequest) -> HttpResponse:
    return render(request, "", context={})
