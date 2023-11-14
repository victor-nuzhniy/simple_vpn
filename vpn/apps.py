"""Vpn app configuration."""
from django.apps import AppConfig


class VpnConfig(AppConfig):
    """AppConfig for vpn app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "vpn"
