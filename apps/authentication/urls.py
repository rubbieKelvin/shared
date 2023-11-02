from django.urls import path
from . import views

urlpatterns = [
    path("accounts/signup", views.signup_page, name="shared_auth_signup"),
    path("accounts/signin", views.login_page, name="shared_auth_signin"),
]
