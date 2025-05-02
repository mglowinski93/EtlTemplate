import pytest

from ..common import annotations
from . import fakers


@pytest.fixture
def test_extract_unit_of_work() -> (
    annotations.YieldFixture[fakers.TestExtractUnitOfWork]
):
    test_unit_of_work = fakers.TestExtractUnitOfWork()
    yield test_unit_of_work


@pytest.fixture
def test_data_unit_of_work() -> annotations.YieldFixture[fakers.TestSaveDataUnitOfWork]:
    test_unit_of_work = fakers.TestSaveDataUnitOfWork()
    yield test_unit_of_work


@pytest.fixture
def test_data_query_repository() -> (
    annotations.YieldFixture[fakers.TestDataQueryRepository]
):
    yield fakers.TestDataQueryRepository()
