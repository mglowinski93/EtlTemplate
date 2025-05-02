import pytest
from django.db import DatabaseError
from pytest_mock import MockFixture

from infrastructures.apps.common import exceptions as common_exceptions
from infrastructures.apps.load import models
from modules.common import pagination as pagination_dtos
from modules.load.domain import ports, value_objects
from modules.load.services import queries
from modules.load.services.queries import ports as query_ports
from modules.load.services.queries import queries as query_dtos
from modules.load.services.queries.ports import repositories as query_repositories

from ..... import fakers as common_fakers
from ..... import model_factories


def test_django_data_domain_repository_create_method_creates_records(
    django_data_domain_repository: ports.AbstractDataDomainRepository,
):
    # Given
    records_number = 5
    data = [common_fakers.fake_transformed_data() for _ in range(records_number)]

    # When
    django_data_domain_repository.create(data)

    # Then
    assert models.Data.objects.filter().count() == records_number
    assert all(
        models.Data.objects.filter(
            data__contains={"full_name": data.full_name}
        ).exists()
        for data in data
    )


def test_django_data_domain_repository_create_method_raises_custom_exception_on_database_exception(
    mocker: MockFixture,
    django_data_domain_repository: ports.AbstractDataDomainRepository,
):
    # Given
    side_effect = DatabaseError
    mocker.patch.object(
        models.Data.objects,
        "bulk_create",
        side_effect=side_effect,
    )

    # When and then
    with pytest.raises(common_exceptions.DatabaseError):
        django_data_domain_repository.create([common_fakers.fake_transformed_data()])
    assert not models.Data.objects.exists()


def test_django_data_query_repository_get_method_returns_detailed_record_when_record_exists(
    django_data_query_repository: query_repositories.AbstractDataQueryRepository,
):
    # Given
    data: models.Data = model_factories.DataFactory.create()

    # When
    result = django_data_query_repository.get(
        value_objects.DataId.from_hex(data.id.hex)
    )

    # Then
    assert result.id == data.id
    assert isinstance(result, queries.DetailedOutputData)


def test_django_data_query_repository_get_method_raises_custom_exception_on_database_exception(
    mocker: MockFixture,
    django_data_query_repository: query_repositories.AbstractDataQueryRepository,
):
    # Given
    mocker.patch.object(
        models.Data.objects,
        "get",
        side_effect=DatabaseError,
    )

    # When and then
    with pytest.raises(common_exceptions.DatabaseError):
        django_data_query_repository.get(data_id=value_objects.DataId.new())


def test_django_data_query_repository_get_method_raises_data_does_not_exist_when_data_not_found(
    mocker: MockFixture,
    django_data_query_repository: query_repositories.AbstractDataQueryRepository,
):
    # Given
    mocker.patch.object(
        models.Data.objects,
        "get",
        side_effect=models.Data.DoesNotExist,
    )

    # When and then
    with pytest.raises(common_exceptions.DataDoesNotExist):
        django_data_query_repository.get(data_id=value_objects.DataId.new())


def test_django_data_query_repository_list_method_queries_all_records(
    django_data_query_repository: query_repositories.AbstractDataQueryRepository,
):
    # Given
    data_number = 5
    model_factories.DataFactory.create_batch(size=data_number)

    # When
    results, count = django_data_query_repository.list(
        filters=query_ports.DataFilters(),
        ordering=query_ports.DataOrdering(),
        pagination=pagination_dtos.Pagination(
            offset=pagination_dtos.PAGINATION_DEFAULT_OFFSET,
            records_per_page=pagination_dtos.PAGINATION_DEFAULT_LIMIT,
        ),
    )

    # Then
    assert count == data_number
    assert isinstance(results, list)
    assert all(isinstance(result, query_dtos.OutputData) for result in results)


def test_django_data_query_repository_list_method_raises_custom_exception_on_database_exception(
    mocker: MockFixture,
    django_data_query_repository: query_repositories.AbstractDataQueryRepository,
):
    # Given
    side_effect = DatabaseError
    mocker.patch.object(
        models.Data.objects,
        "filter",
        side_effect=side_effect,
    )

    # When and then
    with pytest.raises(common_exceptions.DatabaseError):
        django_data_query_repository.list(
            filters=query_ports.DataFilters(),
            ordering=query_ports.DataOrdering(),
            pagination=pagination_dtos.Pagination(
                offset=pagination_dtos.PAGINATION_DEFAULT_OFFSET,
                records_per_page=pagination_dtos.PAGINATION_DEFAULT_LIMIT,
            ),
        )
