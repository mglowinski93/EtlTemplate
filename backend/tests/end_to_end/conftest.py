import pytest
from rest_framework.test import APIClient

from ..common.annotations import YieldFixture
from ..common.conftest import enable_db_access  # noqa: F401
from .dtos import APIClientData, User


@pytest.fixture
def unauthenticated_client() -> YieldFixture[APIClientData]:
    yield APIClientData(APIClient(), User)
