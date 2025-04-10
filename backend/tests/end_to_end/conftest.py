import pytest
from ..common.annotations import YieldFixture
from rest_framework.test import APIClient
from .dtos import APIClientData, User

@pytest.fixture
def unauthenticated_client() -> YieldFixture[APIClientData]:
    yield APIClientData(APIClient(), User)
                     
