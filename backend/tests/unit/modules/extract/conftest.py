import pytest

from ....common.annotations import YieldFixture
from . import fakers


@pytest.fixture
def test_extract_unit_of_work() -> YieldFixture[fakers.TestExtractUnitOfWork]:
    test_unit_of_work = fakers.TestExtractUnitOfWork()
    yield test_unit_of_work
