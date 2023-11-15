"""Urls for vpn app."""
from django.contrib.auth.views import LogoutView
from django.urls import path

from vpn.views import CustomLoginView, CustomPasswordChangeView, RegisterView

app_name = "vpn"

urlpatterns = [
    path("sign-up/", RegisterView.as_view(), name="sign_up"),
    path("sign-in/", CustomLoginView.as_view(), name="sign_in"),
    path("logout/", LogoutView.as_view(next_page="vpn:sign_up"), name="logout"),
    path(
        "password-change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
]
