import pytest

from ..common.annotations import YieldFixture
from . import fakers


@pytest.fixture
def test_extract_unit_of_work() -> YieldFixture[fakers.TestExtractUnitOfWork]:
    test_unit_of_work = fakers.TestExtractUnitOfWork()
    test_unit_of_work.file = fakers.TestFileDomainRepository()
    test_unit_of_work.extract = fakers.TestExtractDomainRepository()
    yield test_unit_of_work


@pytest.fixture
def test_data_unit_of_work() -> YieldFixture[fakers.TestSaveDataUnitOfWork]:
    test_unit_of_work = fakers.TestSaveDataUnitOfWork()
    test_unit_of_work.data = fakers.TestDataDomainRepository()
    yield test_unit_of_work


@pytest.fixture
def test_data_query_repository() -> YieldFixture[fakers.TestDataQueryRepository]:
    yield fakers.TestDataQueryRepository()
