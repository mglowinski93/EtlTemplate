import pytest

from ....common.annotations import YieldFixture
from . import fakers


@pytest.fixture
def test_data_unit_of_work() -> YieldFixture[fakers.TestSaveDataUnitOfWork]:
    test_unit_of_work = fakers.TestSaveDataUnitOfWork()
    test_unit_of_work.data = fakers.TestDataDomainRepository()
    yield test_unit_of_work
