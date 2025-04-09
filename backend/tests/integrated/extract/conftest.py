import pytest

from tests.common.annotations import YieldFixture
from infrastructures.apps.extract.adapters import DjangoFileDomainRepository
# from . import fakers


@pytest.fixture
def test_extract_django_domain_repository() -> YieldFixture[DjangoFileDomainRepository]:
    yield DjangoFileDomainRepository()
