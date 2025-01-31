import pytest

from infrastructures.apps.load.adapters.repositories import (
    DjangoDataDomainRepository,
    DjangoDataQueryRepository,
)

from ....common import annotations


@pytest.fixture
def django_data_domain_repository() -> (
    annotations.YieldFixture[DjangoDataDomainRepository]
):
    yield DjangoDataDomainRepository()


@pytest.fixture
def django_data_query_repository() -> (
    annotations.YieldFixture[DjangoDataQueryRepository]
):
    yield DjangoDataQueryRepository()
