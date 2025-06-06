from datetime import datetime
from http import HTTPStatus
from typing import Any
from uuid import UUID

import pytest

from infrastructures.apps.common import consts as infrastructure_common_consts
from infrastructures.apps.load.views import serializers

from ..... import model_factories
from ....dtos import APIClientData
from ....utils import get_url
from . import fakers


def test_get_data_endpoint_returns_data_when_specified_data_exists(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    data = model_factories.DataFactory.create()

    # When
    response = client.get(get_url(path_name="load-detail", path_params={"pk": data.id}))

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response: dict[str, Any] = response.data
    assert serializers.DetailedOutputDataReadSerializer(data=json_response).is_valid()

    timestamp = datetime.fromisoformat(json_response["timestamp"])
    assert timestamp == data.created_at
    assert (
        timestamp.tzinfo is not None
        and timestamp.tzinfo.utcoffset(timestamp) is not None
    )


def test_get_data_endpoint_returns_404_when_specified_data_does_not_exist(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    data_id = fakers.fake_data_id()

    # When
    response = client.get(get_url(path_name="load-detail", path_params={"pk": data_id}))

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert infrastructure_common_consts.ERROR_DETAIL_KEY in response.data


def test_get_data_endpoint_returns_404_when_data_id_has_invalid_format(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    data_id = "invalid-format-data-id"

    # When
    response = client.get(get_url(path_name="load-detail", path_params={"pk": data_id}))

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert infrastructure_common_consts.ERROR_DETAIL_KEY in response.data


def test_list_data_endpoint_returns_empty_list_when_no_data_exists(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

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
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    data_number = 3
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

    assert infrastructure_common_consts.PAGINATION_NEXT_LINK_NAME in json_response
    assert infrastructure_common_consts.PAGINATION_PREVIOUS_LINK_NAME in json_response

    assert infrastructure_common_consts.PAGINATION_RESULTS_NAME in json_response
    results = json_response[infrastructure_common_consts.PAGINATION_RESULTS_NAME]

    assert isinstance(results, list)
    assert all(
        serializers.OutputDataReadSerializer(data=data).is_valid() for data in results
    )


def test_list_data_endpoint_pagination(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    data_number = 20
    pagination_offset = 1
    pagination_limit = 5
    model_factories.DataFactory.create_batch(data_number)

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={
                infrastructure_common_consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME: pagination_offset,
                infrastructure_common_consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME: pagination_limit,
            },
        ),
    )

    # Then
    assert response.status_code == HTTPStatus.OK

    json_response: dict[str, Any] = response.data
    assert (
        len(json_response[infrastructure_common_consts.PAGINATION_RESULTS_NAME])
        == pagination_limit
    )
    assert infrastructure_common_consts.PAGINATION_NEXT_LINK_NAME in json_response
    assert infrastructure_common_consts.PAGINATION_PREVIOUS_LINK_NAME in json_response
    assert (
        json_response[infrastructure_common_consts.PAGINATION_COUNT_NAME] == data_number
    )


def test_list_data_endpoint_pagination_next_link(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    pagination_limit = 1
    data_1 = model_factories.DataFactory.create()
    data_2 = model_factories.DataFactory.create()

    # When and then
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={
                infrastructure_common_consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME: 0,
                infrastructure_common_consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME: pagination_limit,
            },
        ),
    )

    assert response.status_code == HTTPStatus.OK
    json_response: dict[str, Any] = response.data
    assert infrastructure_common_consts.PAGINATION_NEXT_LINK_NAME in json_response
    assert (
        UUID(
            json_response[infrastructure_common_consts.PAGINATION_RESULTS_NAME][0]["id"]
        )
        == data_1.id
    )
    assert (
        json_response.get(infrastructure_common_consts.PAGINATION_PREVIOUS_LINK_NAME)
        is None
    )
    assert (
        json_response.get(infrastructure_common_consts.PAGINATION_NEXT_LINK_NAME)
        is not None
    )

    # When and then
    response = client.get(
        json_response[infrastructure_common_consts.PAGINATION_NEXT_LINK_NAME]
    )

    assert response.status_code == HTTPStatus.OK
    json_response: dict[str, Any] = response.data  # type: ignore[no-redef]
    assert infrastructure_common_consts.PAGINATION_NEXT_LINK_NAME in json_response
    assert (
        UUID(
            json_response[infrastructure_common_consts.PAGINATION_RESULTS_NAME][0]["id"]
        )
        == data_2.id
    )
    assert (
        json_response.get(infrastructure_common_consts.PAGINATION_PREVIOUS_LINK_NAME)
        is not None
    )
    assert (
        json_response.get(infrastructure_common_consts.PAGINATION_NEXT_LINK_NAME)
        is None
    )


@pytest.mark.parametrize(
    ("pagination_key", "pagination_value"),
    (
        (
            infrastructure_common_consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME,
            "invalid-offset",
        ),
        (
            infrastructure_common_consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME,
            "invalid-records_per_page",
        ),
    ),
)
def test_list_data_endpoint_handles_invalid_pagination_parameters(
    unauthenticated_api_client: APIClientData,
    pagination_key: str,
    pagination_value: str,
):
    # Given
    client = unauthenticated_api_client.client

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={
                pagination_key: pagination_value,
            },
        ),
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert infrastructure_common_consts.ERROR_DETAIL_KEY in response.data


def test_list_data_endpoint_filtering_by_is_satisfied(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    data = model_factories.DataFactory.create(data=fakers.fake_data(is_satisfied=True))
    model_factories.DataFactory.create(data=fakers.fake_data(is_satisfied=False))

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={"is_satisfied": data.data["is_satisfied"]},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.data[infrastructure_common_consts.PAGINATION_COUNT_NAME] == 1
    assert all(
        item["is_satisfied"] == data.data["is_satisfied"]
        for item in response.data[infrastructure_common_consts.PAGINATION_RESULTS_NAME]
    )


def test_list_data_endpoint_filtering_by_timestamp_to(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    data = model_factories.DataFactory.create()
    model_factories.DataFactory.create()

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={"timestamp_to": data.created_at.isoformat()},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.data[infrastructure_common_consts.PAGINATION_COUNT_NAME] == 1
    assert all(
        datetime.fromisoformat(item["timestamp"]) >= data.created_at
        for item in response.data[infrastructure_common_consts.PAGINATION_RESULTS_NAME]
    )


def test_list_data_endpoint_filtering_by_timestamp_from(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    model_factories.DataFactory.create()
    data = model_factories.DataFactory.create()

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={"timestamp_from": data.created_at.isoformat()},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.data[infrastructure_common_consts.PAGINATION_COUNT_NAME] == 1
    assert all(
        datetime.fromisoformat(item["timestamp"]) <= data.created_at
        for item in response.data[infrastructure_common_consts.PAGINATION_RESULTS_NAME]
    )


def test_list_data_endpoint_filtering_by_a_few_attributes(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    model_factories.DataFactory.create(data=fakers.fake_data(is_satisfied=False))
    data = model_factories.DataFactory.create(data=fakers.fake_data(is_satisfied=False))
    data2 = model_factories.DataFactory.create(data=fakers.fake_data(is_satisfied=True))
    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={
                "timestamp_from": data.created_at.isoformat(),
                "timestamp_to": data2.created_at.isoformat(),
                "is_satisfied": True,
            },
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.data[infrastructure_common_consts.PAGINATION_COUNT_NAME] == 1
    assert all(
        datetime.fromisoformat(item["timestamp"]) <= data2.created_at
        for item in response.data[infrastructure_common_consts.PAGINATION_RESULTS_NAME]
    )


@pytest.mark.parametrize(
    ("filter_key", "filter_value"),
    (
        ("is_satisfied", "invalid-type"),
        ("timestamp_from", "invalid-datetime"),
        ("timestamp_to", "invalid-datetime"),
    ),
)
def test_list_data_endpoint_returns_400_when_invalid_value_passed_as_query_filter_parameter(
    unauthenticated_api_client: APIClientData, filter_key: str, filter_value: str
):
    # Given
    client = unauthenticated_api_client.client

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={filter_key: filter_value},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert infrastructure_common_consts.ERROR_DETAIL_KEY in response.data


def test_list_data_endpoint_skip_unsupported_query_parameter(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={"invalid-query-parameter": "invalid-value"},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "order_by", ("full_name", "-full_name", "timestamp", "-timestamp")
)
def test_list_data_endpoint_ordering(
    unauthenticated_api_client: APIClientData, order_by: str
):
    # Given
    client = unauthenticated_api_client.client

    batch_size = 5
    model_factories.DataFactory.create_batch(batch_size)

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={"ordering": order_by},
        )
    )

    # Then
    compare_key = order_by[1:] if order_by.startswith("-") else order_by
    assert response.status_code == HTTPStatus.OK
    results = response.data[infrastructure_common_consts.PAGINATION_RESULTS_NAME]
    assert results == sorted(
        results,
        key=lambda x: x[compare_key],
        reverse=order_by.startswith("-"),
    )


def test_list_data_endpoint_ordering_by_a_few_attributes(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    batch_size = 5
    model_factories.DataFactory.create_batch(batch_size)

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={"ordering": "timestamp,full_name"},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    results = response.data[infrastructure_common_consts.PAGINATION_RESULTS_NAME]
    assert [(data["timestamp"], data["full_name"]) for data in results] == [
        (data["timestamp"], data["full_name"])
        for data in sorted(
            results,
            key=lambda item: (item["timestamp"], item["full_name"]),
        )
    ]


def test_list_data_endpoint_ordering_skip_unsupported_ordering(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    # When
    response = client.get(
        get_url(
            path_name="load-list",
            query_params={"ordering": "invalid-value"},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
