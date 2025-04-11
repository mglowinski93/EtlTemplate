from ...conftest import APIClientData
from ...utils import get_url
from http import HTTPStatus
from typing import Any
from infrastructures.apps.common import const as infrastructure_common_consts
from infrastructures.apps.load.views import serializers



def test_list_todo_endpoint_returns_all_existing_datas(unauthenticated_client: APIClientData):
    # Given
    client = unauthenticated_client.client

    # When
    response = client.get(get_url("load"))

    # Then
    assert response.status_code == HTTPStatus.OK

    results: dict[str, Any] = response.data

    assert isinstance(results, list)
    assert all(serializers.DetailedOutputDataReadSerializer(data=detailed_output_data).is_valid() for detailed_output_data in results)
