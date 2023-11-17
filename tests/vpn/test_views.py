"""Module for testing vpn app views."""
from typing import Tuple

import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.test import Client
from django.urls import reverse
from faker import Faker

from tests.vpn.factories import PageFactory, PageLinksFactory, PersonalSiteFactory


@pytest.mark.django_db
class TestIndexView:
    """Class for testing IndexView."""

    pytestmark = pytest.mark.django_db

    def test_get_method(self, client: Client) -> None:
        """Test IndexView get method."""
        url = reverse("vpn:index")
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["title"] == "Welcome"


@pytest.mark.django_db
class TestRegisterView:
    """Class for testing RegisterView."""

    pytestmark = pytest.mark.django_db

    def test_get_method(self, client: Client) -> None:
        """Test RegisterView get method."""
        url = reverse("vpn:sign_up")
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["title"] == "Sign up"

    def test_post_method(self, faker: Faker, client: Client) -> None:
        """Test RegisterView post method."""
        url = reverse("vpn:sign_up")
        password = faker.pystr(min_chars=15, max_chars=20)
        data = {
            "username": faker.user_name(),
            "password1": password,
            "password2": password,
        }
        response = client.post(url, data=data)
        assert response.status_code == 302
        assert User.objects.get(username=data.get("username")) is not None


@pytest.mark.django_db
class TestLoginView:
    """Class for testing LoginView."""

    pytestmark = pytest.mark.django_db

    def test_get_method(self, client: Client) -> None:
        """Test LoginView get method."""
        url = reverse("vpn:sign_in")
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["title"] == "Sign in"

    def test_post_method(
        self, faker: Faker, client: Client, get_admin_user_data: Tuple
    ) -> None:
        """Test LoginView post method."""
        username, password = get_admin_user_data
        data = {
            "username": username,
            "password": password,
        }
        url = reverse("vpn:sign_in")
        response = client.post(url, data=data)
        assert response.status_code == 302


@pytest.mark.django_db
class TestPasswordChangeView:
    """Class for testing PasswordChangeView."""

    pytestmark = pytest.mark.django_db

    def test_get_method(self, client: Client, get_admin_user_data: Tuple) -> None:
        """Test PasswordChangeView get method."""
        username, password = get_admin_user_data
        client.login(username=username, password=password)
        url = reverse("vpn:password_change")
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["title"] == "Password change"

    def test_post_method(
        self, faker: Faker, client: Client, get_admin_user_data: Tuple
    ) -> None:
        """Test PasswordChangeView post method."""
        username, password = get_admin_user_data
        client.login(username=username, password=password)
        data = {
            "old_password": password,
            "new_password1": "test_new_password",
            "new_password2": "test_new_password",
        }
        url = reverse("vpn:password_change")
        response = client.post(url, data=data)
        assert response.status_code == 302
        client.logout()
        assert client.login(username=username, password="test_new_password")


@pytest.mark.django_db
class TestAccountView:
    """Class for testing AccountView."""

    pytestmark = pytest.mark.django_db

    def test_get_method(self, client: Client, get_admin_user_data: Tuple) -> None:
        """Test AccountView get method."""
        username, password = get_admin_user_data
        user = User.objects.get(username=username)
        with transaction.atomic():
            personal_sites = PersonalSiteFactory.create_batch(size=4)
            for site in personal_sites:
                site.owner = user
                site.save()
            pages = PageFactory.create_batch(size=4)
            for i, site in enumerate(personal_sites):
                pages[i].personal_site = site
                pages[i].save()
        client.login(username=username, password=password)
        url = reverse("vpn:account", kwargs={"pk": user.id})
        response = client.get(url)
        expected_sites = response.context["personal_sites"]
        expected_pages = response.context["pages"]
        assert response.status_code == 200
        assert response.context["title"] == "Personal info"
        for i, site in enumerate(personal_sites):
            assert site == expected_sites[i]
        for i, page in enumerate(pages):
            assert page == expected_pages[i]


@pytest.mark.django_db
class TestPageView:
    """Class for testing PageView."""

    pytestmark = pytest.mark.django_db

    def test_get_method(self, client: Client) -> None:
        """Test PageView get method."""
        personal_site = PersonalSiteFactory()
        page = PageFactory(personal_site=personal_site)
        page_link = PageLinksFactory(page=page)
        url = reverse(
            "vpn:page", kwargs={"site_slug": personal_site.slug, "slug": page.slug}
        )
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["title"] == page.name
        assert response.context["page"] == page
        assert response.context["links"][0] == page_link.link
