import typing
from furl import furl
from pydantic import BaseModel
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model
from django.views import View
from django.forms import Form
from .models import ExtensibleUser

try:
    from knox.models import AuthToken, AuthTokenManager
except ImportError:
    raise ImportError(
        "Django rest knox required for this feature. https://jazzband.github.io/django-rest-knox/"
    )


from .settings import AuthConf


class CallbackParams(BaseModel):
    code: str
    user: str
    created: typing.Literal[1, 0]


def login_and_redirect(
    user: ExtensibleUser, config: AuthConf, created: typing.Literal[1, 0] = 0
):
    # Create a Knox token for the authenticated user
    knox_token_manager: AuthTokenManager = typing.cast(
        AuthTokenManager, AuthToken.objects
    )
    _, token = knox_token_manager.create(user=user)

    callback_data = CallbackParams(code=token, created=created, user=str(user.pk))

    # https://github.com/gruns/furl/
    url_obj = furl(config.callback_url)
    url_obj.set(query=callback_data.model_dump())

    return redirect(url_obj.url)


class SignupView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        config = AuthConf.from_settings()

        return render(
            request,
            "authentication/signup.html",
            {
                "config": config,
                "form": config.signup_form(),
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        config = AuthConf.from_settings()
        form = config.signup_form(request.POST)

        if not form.is_valid():
            return render(
                request,
                "authentication/signup.html",
                {"config": config, "form": form},
            )

        data: dict[str, typing.Any] = form.cleaned_data
        User = typing.cast(type[ExtensibleUser], get_user_model())

        assert issubclass(
            User, ExtensibleUser
        ), "For compactibility, ensure your user model subclasses shared.apps.authentication.models.ExtensibleUser"

        if User.objects.filter(
            **{config.username_field: data[config.username_field]}
        ).exists():
            return render(
                request,
                "authentication/signup.html",
                {
                    "config": config,
                    "form": form,
                    "flash_error": "User already exists",
                },
            )

        user_create_fields = set(data.keys()).difference(
            config.exclude_fields_on_create
        )

        user = User.objects.create_user(**{k: data[k] for k in user_create_fields})

        return login_and_redirect(user, config, created=1)


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        config = AuthConf.from_settings()

        return render(
            request,
            "authentication/login.html",
            {
                "config": config,
                "form": config.login_form(),
            },
        )

    def _return_with_flash(
        self, request, flash: str, config: AuthConf, form: Form
    ) -> HttpResponse:
        return render(
            request,
            "authentication/login.html",
            {
                "config": config,
                "form": form,
                "flash_error": flash,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        config = AuthConf.from_settings()
        form = config.login_form(request.POST)

        if not form.is_valid():
            return render(
                request,
                "authentication/login.html",
                {"config": config, "form": form},
            )

        data: dict[str, typing.Any] = form.cleaned_data
        User = typing.cast(type[ExtensibleUser], get_user_model())

        user = User.objects.filter(
            **{config.username_field: data[config.username_field]}
        ).first()

        if user == None:
            return self._return_with_flash(
                request,
                f"User with that {config.username_field} does not exist",
                config,
                form,
            )

        user = typing.cast(ExtensibleUser, user)

        if not user.check_password(data["password"]):
            return self._return_with_flash(request, "Incorrect password", config, form)

        return login_and_redirect(user, config)


def logout_page(request: HttpRequest) -> HttpResponse:
    return render(request, "", context={})
