"""Urls for vpn app."""
from django.urls import path

from vpn.views import RegisterView

app_name = "vpn"

urlpatterns = [
    path("sign_up/", RegisterView.as_view(), name="sign_up"),
]
