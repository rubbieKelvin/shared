from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .settings import AuthConf


def signup_page(request: HttpRequest) -> HttpResponse:
    config = AuthConf.from_settings()

    return render(
        request,
        "authentication/signup.html",
        {"config": config, "fields": config.signup_fields},
    )


def login_page(request: HttpRequest) -> HttpResponse:
    config = AuthConf.from_settings()

    return render(
        request,
        "authentication/login.html",
        {"config": config, "fields": config.login_fields},
    )


def logout_page(request: HttpRequest) -> HttpResponse:
    return render(request, "", context={})
