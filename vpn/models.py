"""Vpn app models."""
from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models


class PersonalSite(models.Model):
    """Model for user site."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Site owner")
    name = models.CharField(max_length=100, verbose_name="Site name")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Site slug")

    def __str__(self) -> str:
        """Represent model."""
        return f"{self.owner} {self.name}"


class Page(models.Model):
    """Model for site page."""

    name = models.CharField(max_length=100, verbose_name="Page name")
    slug = models.SlugField(max_length=100, verbose_name="Page slug")
    personal_site = models.ForeignKey(
        PersonalSite,
        to_field="slug",
        on_delete=models.CASCADE,
        verbose_name="Personal site",
    )
    sended = models.BigIntegerField(default=0, verbose_name="Sended data")
    loaded = models.BigIntegerField(default=0, verbose_name="Loaded data")
    content = models.TextField(null=True, blank=True, verbose_name="Page content")
    links = models.ManyToManyField(
        "self",
        blank=True,
        through="PageLinks",
        through_fields=("page", "link"),
        verbose_name="Links on page",
    )

    class Meta:
        """Class Meta for Page model."""

        unique_together = ["slug", "personal_site"]

    def __str__(self) -> str:
        """Represent model."""
        return f"{self.personal_site} {self.name}"


class PageLinks(models.Model):
    """Model for 'many-to-many' relationships to self Page model."""

    page = models.ForeignKey(
        Page, related_name="+", on_delete=models.CASCADE, verbose_name="Page with link"
    )
    link = models.ForeignKey(
        Page,
        related_name="page_links",
        on_delete=models.CASCADE,
        verbose_name="Link to page",
    )
    quantity = models.IntegerField(default=0, verbose_name="Links was used")

    def __str__(self) -> str:
        """Represent model."""
        return f"From {self.page} to {self.link}"
