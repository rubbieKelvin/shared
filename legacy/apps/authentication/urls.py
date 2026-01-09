from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.SignupView.as_view(), name="shared_auth_signup"),
    path("login", views.LoginView.as_view(), name="shared_auth_signin"),
    *views.api_endpoints.paths,
]
