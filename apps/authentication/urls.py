from django.urls import path
from . import views

urlpatterns = [
    path("accounts/signup", views.SignupView.as_view(), name="shared_auth_signup"),
    path("accounts/signin", views.LoginView.as_view(), name="shared_auth_signin"),
]
