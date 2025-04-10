import pytest
from django.conf import settings

from ..common.annotations import YieldFixture


@pytest.fixture(autouse=True)
def enable_db_access(transactional_db) -> YieldFixture:
    # Enable database access for all tests.
    yield


@pytest.fixture(autouse=True)
def set_test_media_directory(
    tmp_path,
):
    settings.MEDIA_ROOT = str(tmp_path)
