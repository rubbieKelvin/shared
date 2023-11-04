import typing
from pydantic import BaseModel
from django.conf import settings
from django import forms


class BasicLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email address"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )


class BasicSignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email address"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}), min_length=6
    )


class AuthConf(BaseModel):
    class Customisation(BaseModel):
        background_color: str | None = "rgb(170, 206, 237)"
        wapper_background_color: str | None = "rgb(255, 255, 255)"
        wrapper_border_radius: str | None = "16px"
        widget_border_radius: str | None = "8px"
        wrapper_elevation: str | None = "3em"
        accent: str | None = "rgb(46, 109, 236)"
        accent_hover: str | None = "rgb(29, 97, 235)"
        accent_active: str | None = "rgb(8, 59, 162)"
        text_color: str | None = "#1e212a"
        button_text_color: str | None = "#fff"

    company_name: str | None = None
    application_name: str
    application_url: str
    application_icon_url: str
    callback_url: str
    login_form: type[forms.Form] = BasicLoginForm
    signup_form: type[forms.Form] = BasicSignupForm
    username_field: str = "email"  # could be 'id'
    exclude_fields_on_create: list[
        str
    ] = []  # fields we dont want to pass into the user model
    customisation: Customisation = Customisation()

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
