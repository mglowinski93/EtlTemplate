import pytest
from django.test import Client
from rest_framework.test import APIClient

from .. import model_factories
from ..common import annotations
from ..common.conftest import enable_db_access  # noqa: F401
from .dtos import APIClientData, User


@pytest.fixture
def unauthenticated_api_client() -> annotations.YieldFixture[APIClientData]:
    yield APIClientData(APIClient(), User)


@pytest.fixture
def authenticated_staff_client() -> annotations.YieldFixture[Client]:
    user = model_factories.UserFactory.create(is_staff=True)

    client = Client()
    client.force_login(user)
    yield client
