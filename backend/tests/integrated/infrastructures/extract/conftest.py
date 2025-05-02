import pytest

from infrastructures.apps.extract.adapters.repositories import (
    DjangoExtractDomainRepository,
    DjangoFileDomainRepository,
)

from ....common import annotations


@pytest.fixture
def test_django_file_domain_repository() -> (
    annotations.YieldFixture[DjangoFileDomainRepository]
):
    yield DjangoFileDomainRepository()


@pytest.fixture
def test_django_extract_domain_repository() -> (
    annotations.YieldFixture[DjangoExtractDomainRepository]
):
    yield DjangoExtractDomainRepository()
