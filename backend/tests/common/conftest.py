import pytest

from ..common.annotations import YieldFixture


@pytest.fixture(autouse=True)
def enable_db_access(transactional_db) -> YieldFixture:
    # Enable database access for all tests.
    yield
