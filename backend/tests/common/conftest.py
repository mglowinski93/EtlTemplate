import pytest
from django.conf import settings

from ..common import annotations


@pytest.fixture(autouse=True)
def enable_db_access(transactional_db) -> annotations.YieldFixture:
    # Enable database access for all tests.
    yield


@pytest.fixture(autouse=True)
def set_test_media_root_directory(
    tmp_path,
):
    settings.MEDIA_ROOT = str(tmp_path)
