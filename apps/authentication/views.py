from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .settings import AuthConf


def signup_page(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "authentication/signup.html",
    )


def login_page(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "authentication/login.html",
        {"config": AuthConf.from_settings()},
    )


def logout_page(request: HttpRequest) -> HttpResponse:
    return render(request, "", context={})
