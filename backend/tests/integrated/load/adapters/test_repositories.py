from modules.load.domain import ports, value_objects
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
    data_entity = [transform_value_objects.OutputData(full_name="full name", age=10, is_satisfied= True)]

    # When
    test_django_data_domain_repository.create(data_entity)

    # Then
    assert all(models.Data.objects.filter(data__contains={"full_name": data.full_name}).exists() for data in data_entity)



def test_django_data_domain_repository_create_method_raises_custom_exception_on_django_exception(
    mocker: MockFixture,
    test_django_data_domain_repository: ports.AbstractDataDomainRepository,
):
    # Given
    data_entity = [transform_value_objects.OutputData(full_name="full name", age=10, is_satisfied= True)]
    side_effect = DatabaseError
    mocker.patch(
        "infrastructures.apps.load.models.Data.objects.bulk_create",
        side_effect=side_effect,
    )
    # When and Then
    with pytest.raises(common_exceptions.DatabaseError):
        test_django_data_domain_repository.create(data_entity)
