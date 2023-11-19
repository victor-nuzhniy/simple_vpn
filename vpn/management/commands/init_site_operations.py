"""Module for creating superuser command on empty db."""
import os
from typing import Any

from django.contrib.sites.models import Site
from django.core.management import BaseCommand
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    """Modify site table info in db."""

    def handle(self, *args: Any, **options: Any) -> None:
        """Rename existed and create additional site for vpn."""
        name_1: str = os.getenv("SITE_NAME_1") if os.getenv("SITE_NAME_1") else "1"
        name_2: str = os.getenv("SITE_NAME_2") if os.getenv("SITE_NAME_2") else "2"
        domain_1: str = os.getenv("DOMAIN_1") if os.getenv("DOMAIN_1") else "d1"
        domain_2: str = os.getenv("DOMAIN_2") if os.getenv("DOMAIN_2") else "d2"
        if len(sites := Site.objects.all()) == 1:
            sites[0].name = name_1
            sites[0].domain = domain_1
            sites[0].save()
            Site.objects.create(name=name_2, domain=domain_2)
            print("Sites were successfully created!")
        print("Sites are already exist.")
