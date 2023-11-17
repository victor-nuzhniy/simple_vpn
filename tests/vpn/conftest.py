"""Fixtures for testing vpn app."""
from typing import Dict, Tuple

import pytest
from django.contrib.auth.models import User
from faker import Faker


@pytest.fixture
def get_admin_user_data(faker: Faker, django_user_model: User) -> Tuple[User, Dict]:
    """Create and get authorized user data for testing."""
    username = faker.user_name()
    password = faker.pystr(min_chars=10, max_chars=20)
    user = django_user_model.objects.create_superuser(
        username=username, email="test@gmail.com"
    )
    user.set_password(password)
    user.save()
    return username, password
