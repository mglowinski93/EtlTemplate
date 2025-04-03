import pytest

from ....common.annotations import YieldFixture
from .fakers import TestDataDomainRepository, TestSaveDataUnitOfWork


@pytest.fixture
def test_data_repository() -> YieldFixture[TestDataDomainRepository]:
    yield TestDataDomainRepository()


@pytest.fixture
def test_data_unit_of_work(
    test_data_repository,
) -> YieldFixture[TestSaveDataUnitOfWork]:
    test_unit_of_work = TestSaveDataUnitOfWork()
    test_unit_of_work.data = test_data_repository
    yield test_unit_of_work
