import pytest
from rest_framework.test import APIClient

from ..common.annotations import YieldFixture
from ..common.conftest import enable_db_access  # noqa: F401
from .dtos import APIClientData, User 
from django.test import Client
from ..model_factories import UserFactory

@pytest.fixture
def unauthenticated_client() -> YieldFixture[APIClientData]:
    yield APIClientData(APIClient(), User)

@pytest.fixture
def authenticated_client() -> YieldFixture[APIClientData]:
    user = UserFactory.create(
        is_staff=True,
        is_superuser=True,        
    )

    client = Client()
    client.force_login(user)
    yield client
