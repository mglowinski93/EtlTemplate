import pytest

from ....common.annotations import YieldFixture
from .fakers import (
    TestExtractDomainRepository,
    TestExtractUnitOfWork,
    TestFileDomainRepository,
)


@pytest.fixture
def test_data_unit_of_work() -> YieldFixture[TestExtractUnitOfWork]:
    test_unit_of_work = TestExtractUnitOfWork()
    test_unit_of_work.file = TestFileDomainRepository()
    test_unit_of_work.extract = TestExtractDomainRepository()
    yield test_unit_of_work
