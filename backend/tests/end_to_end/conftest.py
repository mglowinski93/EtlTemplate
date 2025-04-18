import pytest
from django.test import Client
from rest_framework.test import APIClient

from ..common.annotations import YieldFixture
from ..common.conftest import enable_db_access  # noqa: F401
from ..model_factories import UserFactory
from .dtos import APIClientData, User


@pytest.fixture
def unauthenticated_client() -> YieldFixture[APIClientData]:
    yield APIClientData(APIClient(), User)


@pytest.fixture
def authenticated_client() -> YieldFixture[Client]:
    user = UserFactory.create(
        is_staff=True,
        is_superuser=True,
    )

    client = Client()
    client.force_login(user)
    yield client
