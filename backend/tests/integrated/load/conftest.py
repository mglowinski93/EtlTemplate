import pytest

from infrastructures.apps.load.adapters.repositories import (
    DjangoDataDomainRepository,
    DjangoDataQueryRepository
)
from tests.common.annotations import YieldFixture


@pytest.fixture
def test_django_data_domain_repository() -> YieldFixture[DjangoDataDomainRepository]:
    yield DjangoDataDomainRepository()


@pytest.fixture
def test_django_data_query_repository() -> (
    YieldFixture[DjangoDataQueryRepository]
):
    yield DjangoDataQueryRepository()
