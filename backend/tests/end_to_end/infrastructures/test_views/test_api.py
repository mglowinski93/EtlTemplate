from http import HTTPStatus

from ...dtos import APIClientData
from ...utils import get_url


def test_health_check_endpoint(unauthenticated_client: APIClientData):
    # Given
    client = unauthenticated_client.client

    # When
    response = client.get(get_url(path_name="health_check"))

    # Then
    assert response.status_code == HTTPStatus.OK
