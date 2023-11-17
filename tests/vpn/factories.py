"""Factories for testing vpn app tables."""

import factory
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from tests.bases import BaseModelFactory
from vpn.models import Page, PageLinks, PersonalSite


class SiteFactory(BaseModelFactory):
    """Factory for testing Site model."""

    class Meta:
        """Class Meta for SiteFactory."""

        model = Site
        skip_postgeneration_save = True

    domain: str = factory.Faker("domain_name")
    name: str = factory.Faker("pystr")


class UserFactory(BaseModelFactory):
    """Factory for testing User model."""

    class Meta:
        """Class Meta for UserFactory."""

        model = User
        exclude = ("personal_site_set",)
        skip_postgeneration_save = True

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_staff = factory.Faker("pybool")
    is_active = factory.Faker("pybool")
    personal_site_set = factory.RelatedFactoryList(
        factory="tests.app.factories.PersonalSiteFactory",
        factory_related_name="personal_site_set",
        size=0,
    )


class PersonalSiteFactory(BaseModelFactory):
    """Factory for testing PersonalSite model."""

    class Meta:
        """Class Meta for PersonalSiteFactory."""

        model = PersonalSite
        django_get_or_create = ("owner",)
        exclude = ("page_set",)
        skip_postgeneration_save = True

    owner = factory.SubFactory(UserFactory)
    name = factory.Faker("pystr", min_chars=1, max_chars=100)
    slug = factory.Faker("pystr", min_chars=1, max_chars=100)
    page_set = factory.RelatedFactoryList(
        factory="tests.app.factories.PageFactory",
        factory_related_name="page_set",
        size=0,
    )


class PageFactory(BaseModelFactory):
    """Factory for testing Page model."""

    class Meta:
        """Class Meta for PageFactory."""

        model = Page
        django_get_or_create = ("personal_site",)
        exclude = ("page_links",)
        skip_postgeneration_save = True

    name = factory.Faker("pystr", min_chars=1, max_chars=100)
    slug = factory.Faker("pystr", min_chars=1, max_chars=100)
    personal_site = factory.SubFactory(PersonalSiteFactory)
    sended = factory.Faker("pyint")
    loaded = factory.Faker("pyint")
    content = factory.Faker("pystr", max_chars=10000)
    page_links = factory.RelatedFactoryList(
        factory="tests.app.factories.PageLinksFactory",
        factory_related_name="page_links",
        size=0,
    )


class PageLinksFactory(BaseModelFactory):
    """Factory for testing PageLinks model."""

    class Meta:
        """Class Meta for PageLinksFactory."""

        model = PageLinks
        django_get_or_create = ("page", "link")
        skip_postgeneration_save = True

    page = factory.SubFactory(PageFactory)
    link = factory.SubFactory(PageFactory)
    quantity = factory.Faker("pyint")
