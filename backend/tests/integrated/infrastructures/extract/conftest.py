import pytest

from infrastructures.apps.extract.adapters.repositories import (
    DjangoExtractDomainRepository,
    DjangoFileDomainRepository,
)
from tests.common.annotations import YieldFixture


@pytest.fixture
def test_django_file_domain_repository() -> YieldFixture[DjangoFileDomainRepository]:
    yield DjangoFileDomainRepository()


@pytest.fixture
def test_django_extract_domain_repository() -> (
    YieldFixture[DjangoExtractDomainRepository]
):
    yield DjangoExtractDomainRepository()
