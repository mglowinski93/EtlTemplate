import pytest
from django.test import Client
from rest_framework.test import APIClient

from .. import model_factories
from ..common import annotations
from ..common.conftest import enable_db_access  # noqa: F401
from .dtos import APIClientData, ClientData


@pytest.fixture
def unauthenticated_api_client() -> annotations.YieldFixture[APIClientData]:
    yield APIClientData(
        APIClient(),
        model_factories.UserFactory.create(is_staff=False, is_superuser=False),
    )


@pytest.fixture
def authenticated_admin_client() -> annotations.YieldFixture[ClientData]:
    user = model_factories.UserFactory.create(is_staff=True, is_superuser=True)

    client = Client()
    client.force_login(user)

    yield ClientData(client=client, user=user)
