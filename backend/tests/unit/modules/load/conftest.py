import pytest

from ....common.annotations import YieldFixture
from . import fakers


@pytest.fixture
def test_data_unit_of_work() -> YieldFixture[fakers.TestSaveDataUnitOfWork]:
    test_unit_of_work = fakers.TestSaveDataUnitOfWork()
    yield test_unit_of_work


@pytest.fixture
def test_data_query_repository() -> YieldFixture[fakers.TestDataQueryRepository]:
    yield fakers.TestDataQueryRepository()
