import pytest

from ....common import annotations
from . import fakers


@pytest.fixture
def test_extract_unit_of_work() -> (
    annotations.YieldFixture[fakers.TestExtractUnitOfWork]
):
    test_unit_of_work = fakers.TestExtractUnitOfWork()
    yield test_unit_of_work
