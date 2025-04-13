from ....dtos import APIClientData
from ..... import model_factories 
from ....utils import get_url
from http import HTTPStatus
from typing import Any
import pytest
from infrastructures.apps.common import const as infrastructure_common_consts
from datetime import datetime
from infrastructures.apps.load.views import serializers


@pytest.mark.django_db
def test_list_data_endpoint_returns_empty_list_when_no_data_exists(
    unauthenticated_client: APIClientData,
):
    # Given
    client = unauthenticated_client.client

    # When
    response = client.get(
        get_url(path_name="load-list")
    )

    # Then
    assert response.status_code == HTTPStatus.OK

    json_response: dict[str, Any] = response.data
    results = json_response[infrastructure_common_consts.PAGINATION_DATA_NAME]
    assert isinstance(results, list)
    assert not results
    assert json_response[infrastructure_common_consts.PAGINATION_COUNT_NAME] == 0

@pytest.mark.django_db
def test_list_data_endpoint_returns_data_when_data_exists(
    unauthenticated_client: APIClientData,
):
    # Given
    data_number = 3
    client = unauthenticated_client.client
    model_factories.DataFactory.create_batch(data_number)

    # When
    response = client.get(
        get_url(path_name="load-list")
    )

    # Then
    assert response.status_code == HTTPStatus.OK

    json_response: dict[str, Any] = response.data
    assert infrastructure_common_consts.PAGINATION_COUNT_NAME in json_response
    assert (
        json_response[infrastructure_common_consts.PAGINATION_COUNT_NAME]
        == data_number
    )

    assert infrastructure_common_consts.PAGINATION_DATA_NAME in json_response
    results = json_response[infrastructure_common_consts.PAGINATION_DATA_NAME]

    assert isinstance(results, list)
    assert all(serializers.OutputDataReadSerializer(data=data).is_valid() for data in results)

