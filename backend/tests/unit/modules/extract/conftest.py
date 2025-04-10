import pytest

from ....common.annotations import YieldFixture
from . import fakers


@pytest.fixture
def test_extract_unit_of_work() -> YieldFixture[fakers.TestExtractUnitOfWork]:
    test_unit_of_work = fakers.TestExtractUnitOfWork()
    test_unit_of_work.file = fakers.TestFileDomainRepository()
    test_unit_of_work.extract = fakers.TestExtractDomainRepository()
    yield test_unit_of_work
