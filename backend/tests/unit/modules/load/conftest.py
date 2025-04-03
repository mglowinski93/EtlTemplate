import pytest

from ....common.annotations import YieldFixture
from .fakers import TestDataDomainRepository, TestSaveDataUnitOfWork


@pytest.fixture
def test_data_unit_of_work() -> YieldFixture[TestSaveDataUnitOfWork]:
    test_unit_of_work = TestSaveDataUnitOfWork()
    test_unit_of_work.data = TestDataDomainRepository()
    yield test_unit_of_work
