"""Vpn app models."""
from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class PersonalSite(models.Model):
    """Model for user site."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Site owner")
    name = models.SlugField(max_length=100, verbose_name="Site name")
    slug = models.CharField(max_length=100, unique=True, verbose_name="Site slug")

    def __str__(self) -> str:
        """Represent model."""
        return f"{self.owner} {self.name}"

    def save(self, *args, **kwargs) -> None:
        """Create slug from name."""
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Page(models.Model):
    """Model for site page."""

    name = models.CharField(max_length=100, verbose_name="Page name")
    slug = models.SlugField(max_length=100, verbose_name="Page slug")
    personal_site = models.ForeignKey(
        PersonalSite, on_delete=models.CASCADE, verbose_name="Personal site"
    )
    sended = models.FloatField(verbose_name="Sended data")
    loaded = models.FloatField(verbose_name="Loaded data")
    links = models.ManyToManyField(
        "self",
        through="PageLinks",
        through_fields=("page", "link"),
        limit_choices_to={"personal_site": personal_site},
        verbose_name="Links on page",
    )

    def __str__(self) -> str:
        """Represent model."""
        return f"{self.name}"


class PageLinks(models.Model):
    """Model for 'many-to-many' relationships to self Page model."""

    page = models.ForeignKey(
        Page, related_name="+", on_delete=models.CASCADE, verbose_name="Page with link"
    )
    link = models.ForeignKey(
        Page, on_delete=models.CASCADE, verbose_name="Link to page"
    )
    quantity = models.IntegerField(verbose_name="Links was used")

    def __str__(self) -> str:
        """Represent model."""
        return f"From {self.page} to {self.link}"
