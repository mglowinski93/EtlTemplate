import sys
from importlib import reload
from http import HTTPStatus

import pytest
from django.conf import settings
from django.test.utils import override_settings
from django.urls import clear_url_caches, exceptions, reverse

from ...dtos import APIClientData
from ...utils import get_url


@pytest.mark.parametrize("path_name", ["schema", "swagger-ui", "redoc"])
def test_documentation_endpoint_not_available_in_not_development_environment(
    unauthenticated_client: APIClientData, path_name: str
):
    # Given
    client = unauthenticated_client.client

    # When and then
    with pytest.raises(exceptions.NoReverseMatch):
        client.get(get_url(path_name=path_name))


@override_settings(DEBUG=True)
@pytest.mark.parametrize("path_name", ["schema", "swagger-ui", "redoc"])
def test_documentation_endpoint_not_available_in_development_environment(
    unauthenticated_client: APIClientData, path_name: str
):
    # Given
    client = unauthenticated_client.client
    clear_url_caches()
    reload(sys.modules[settings.ROOT_URLCONF])

    # When
    response = client.get(reverse(path_name))

    # Then
    assert response.status_code == HTTPStatus.OK
