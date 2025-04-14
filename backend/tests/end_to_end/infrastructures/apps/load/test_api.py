from datetime import datetime
from http import HTTPStatus
from typing import Any

from infrastructures.apps.common import const as infrastructure_common_consts
from infrastructures.apps.load.views import serializers

from ..... import model_factories
from ....dtos import APIClientData
from ....utils import get_url
from . import fakers


def test_get_data_endpoint_returns_data_when_specified_data_exists(
    unauthenticated_client: APIClientData,
):
    # Given
    client = unauthenticated_client.client

    data = model_factories.DataFactory.create()

    # When
    response = client.get(get_url(path_name="load-detail", path_params={"pk": data.id}))

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response: dict[str, Any] = response.data["data"]
    assert serializers.DetailedOutputDataReadSerializer(data=json_response).is_valid()

    timestamp = datetime.fromisoformat(json_response["timestamp"])
    assert timestamp == data.created_at
    assert (
        timestamp.tzinfo is not None
        and timestamp.tzinfo.utcoffset(timestamp) is not None
    )


def test_get_data_endpoint_returns_404_when_specified_data_does_not_exist(
    unauthenticated_client: APIClientData,
):
    # Given
    client = unauthenticated_client.client
    data_id = fakers.fake_data_id()

    # When
    response = client.get(get_url(path_name="load-detail", path_params={"pk": data_id}))

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert infrastructure_common_consts.ERROR_DETAIL_KEY in response.data


def test_get_data_endpoint_returns_404_when_data_id_has_invalid_format(
    unauthenticated_client: APIClientData,
):
    # Given
    client = unauthenticated_client.client
    data_id = "invalid-format-data-id"

    # When
    response = client.get(get_url(path_name="load-detail", path_params={"pk": data_id}))

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert infrastructure_common_consts.ERROR_DETAIL_KEY in response.data


def test_list_data_endpoint_returns_empty_list_when_no_data_exists(
    unauthenticated_client: APIClientData,
):
    # Given
    client = unauthenticated_client.client

    # When
    response = client.get(get_url(path_name="load-list"))

    # Then
    assert response.status_code == HTTPStatus.OK

    json_response: dict[str, Any] = response.data
    results = json_response[infrastructure_common_consts.PAGINATION_RESULTS_NAME]
    assert isinstance(results, list)
    assert not results
    assert json_response[infrastructure_common_consts.PAGINATION_COUNT_NAME] == 0


def test_list_data_endpoint_returns_data_when_data_exists(
    unauthenticated_client: APIClientData,
):
    # Given
    data_number = 3
    client = unauthenticated_client.client
    model_factories.DataFactory.create_batch(data_number)

    # When
    response = client.get(get_url(path_name="load-list"))

    # Then
    assert response.status_code == HTTPStatus.OK

    json_response: dict[str, Any] = response.data
    assert infrastructure_common_consts.PAGINATION_COUNT_NAME in json_response
    assert (
        json_response[infrastructure_common_consts.PAGINATION_COUNT_NAME] == data_number
    )

    assert infrastructure_common_consts.PAGINATION_RESULTS_NAME in json_response
    results = json_response[infrastructure_common_consts.PAGINATION_RESULTS_NAME]

    assert isinstance(results, list)
    assert all(
        serializers.OutputDataReadSerializer(data=data).is_valid() for data in results
    )
