"""Module for testing vpn app."""

import pytest
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from tests.bases import BaseModelFactory
from tests.vpn.factories import (
    PageFactory,
    PageLinksFactory,
    PersonalSiteFactory,
    SiteFactory,
    UserFactory,
)
from vpn.models import Page, PageLinks, PersonalSite


@pytest.mark.django_db
class TestSite:
    """Class for testing Site model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test Site model instance creation."""
        BaseModelFactory.check_factory(factory_class=SiteFactory, model=Site)

    def test__str__(self) -> None:
        """Test Site __str__ method."""
        obj: Site = SiteFactory()
        expected_result = f"{obj.domain}"
        assert expected_result == obj.__str__()


@pytest.mark.django_db
class TestUser:
    """Class for testing User model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test User model instance creation."""
        BaseModelFactory.check_factory(factory_class=UserFactory, model=User)

    def test__str__(self) -> None:
        """Test User __str__ method."""
        obj: User = UserFactory()
        expected_result = f"{obj.username}"
        assert expected_result == obj.__str__()


@pytest.mark.django_db
class TestPersonalSite:
    """Class for testing PersonalSite model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test PersonalSite model instance creation."""
        BaseModelFactory.check_factory(
            factory_class=PersonalSiteFactory, model=PersonalSite
        )

    def test__str__(self) -> None:
        """Test PersonalSite __str__ method."""
        obj: PersonalSite = PersonalSiteFactory()
        expected_result = f"{obj.owner} {obj.name}"
        assert expected_result == obj.__str__()


@pytest.mark.django_db
class TestPage:
    """Class for testing Page model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test Page model instance creation."""
        BaseModelFactory.check_factory(factory_class=PageFactory, model=Page)

    def test__str__(self) -> None:
        """Test Page __str__ method."""
        obj: Page = PageFactory()
        expected_result = f"{obj.personal_site} {obj.name}"
        assert expected_result == obj.__str__()


@pytest.mark.django_db
class TestPageLinks:
    """Class for testing PageLinks model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test PageLinks model instance creation."""
        BaseModelFactory.check_factory(factory_class=PageLinksFactory, model=PageLinks)

    def test__str__(self) -> None:
        """Test PageLinks __str__ method."""
        obj: PageLinks = PageLinksFactory()
        expected_result = f"From {obj.page} to {obj.link}"
        assert expected_result == obj.__str__()
