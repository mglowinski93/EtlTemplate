from modules.load.domain import ports , value_objects
from modules.load.services.queries.ports import repositories as query_repositories
from modules.load.services.queries import ports as query_ports
from modules.common import pagination as pagination_dtos
from modules.transform.domain import value_objects as transform_value_objects
from infrastructures.apps.load import models
from pytest_mock import MockFixture
from django.db import DatabaseError
import pytest
from infrastructures.apps.common import exceptions as common_exceptions


def test_django_data_domain_repository_create_method_creates_record(
    test_django_data_domain_repository: ports.AbstractDataDomainRepository,
):
    # Given
    #replace with factory
    data_entity = [transform_value_objects.TransformedData(full_name="full name", age=10, is_satisfied= True)]

    # When
    test_django_data_domain_repository.create(data_entity)

    # Then
    assert all(models.Data.objects.filter(data__contains={"full_name": data.full_name}).exists() for data in data_entity)



def test_django_data_domain_repository_create_method_raises_custom_exception_on_django_exception(
    mocker: MockFixture,
    test_django_data_domain_repository: ports.AbstractDataDomainRepository,
):
    # Given
    #replace with factory
    data_entity = [transform_value_objects.TransformedData(full_name="John Snow", age=10, is_satisfied= True)]
    side_effect = DatabaseError
    mocker.patch(
        "infrastructures.apps.load.models.Data.objects.bulk_create",
        side_effect=side_effect,
    )

    # When and Then
    with pytest.raises(common_exceptions.DatabaseError):
        test_django_data_domain_repository.create(data_entity)


def test_django_data_query_repository_list_method_queries_all_records(
    test_django_data_domain_repository: ports.AbstractDataDomainRepository,
    test_django_data_query_repository: query_repositories.AbstractDataQueryRepository,
):
    # Given
    #replace with factory
    data_entity = [transform_value_objects.TransformedData(full_name="John Snow", age=10, is_satisfied= True)]
    test_django_data_domain_repository.create(data_entity)

    # When
    results, count = test_django_data_query_repository.list(
        filters=query_ports.DataFilters(),
        ordering=query_ports.DataOrdering(),
        pagination=pagination_dtos.Pagination(offset=pagination_dtos.PAGINATION_DEFAULT_OFFSET, records_per_page=pagination_dtos.PAGINATION_DEFAULT_LIMIT)
    )

    #Then
    assert count == 1
    assert all(models.Data.objects.filter(data__contains={"full_name": data.full_name}).exists() for data in results)


def test_django_data_query_repository_list_method_raises_custom_exception_on_django_exception(
    mocker: MockFixture,
    test_django_data_query_repository: query_repositories.AbstractDataQueryRepository,
):
    # Given
    side_effect = DatabaseError
    mocker.patch(
        "infrastructures.apps.load.models.Data.objects.filter",
        side_effect=side_effect,
    )

    # When and Then
    with pytest.raises(common_exceptions.DatabaseError):
        test_django_data_query_repository.list(
        filters=query_ports.DataFilters(),
        ordering=query_ports.DataOrdering(),
        pagination=pagination_dtos.Pagination(offset=pagination_dtos.PAGINATION_DEFAULT_OFFSET, records_per_page=pagination_dtos.PAGINATION_DEFAULT_LIMIT)
    )
























#todo fix it
# def test_django_data_query_repository_get_method_returns_detailed_record(
#     test_django_data_domain_repository: ports.AbstractDataDomainRepository,
#     test_django_data_query_repository: query_repositories.AbstractDataQueryRepository,
# ):
#     # Given
#     #replace with factory
#     data_entity = [transform_value_objects.TransformedData(full_name="John Snow", age=10, is_satisfied= True)]    
#     test_django_data_domain_repository.create(data_entity)
#     data: naszModelData = MODel_factory.DataFactory.create()
#     # When
#     result = test_django_data_query_repository.get(naszModelData.DataId) #todo add param id

#     #Then
#     assert all(data.full_name == result.full_name for data in data_entity)



























def test_django_data_query_repository_get_method_raises_custom_exception_when_data_not_found(
    test_django_data_query_repository: query_repositories.AbstractDataQueryRepository,
):
    # Given
    # When and Then
    with pytest.raises(common_exceptions.DataDoesNotExist):
        test_django_data_query_repository.get(data_id=value_objects.DataId.new()) 

def test_django_data_query_repository_get_method_raises_custom_exception_on_django_exception(
    mocker: MockFixture,
    test_django_data_query_repository: query_repositories.AbstractDataQueryRepository,
):
    # Given
    side_effect = DatabaseError
    mocker.patch(
        "infrastructures.apps.load.models.Data.objects.get",
        side_effect=side_effect,
    )

    # When and Then
    with pytest.raises(common_exceptions.DatabaseError):
        test_django_data_query_repository.get(data_id=value_objects.DataId.new()) 
