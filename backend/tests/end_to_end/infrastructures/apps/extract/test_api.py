from http import HTTPStatus
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from ..... import consts
from ....dtos import APIClientData
from ....utils import get_url


@pytest.mark.parametrize(
    "file_path",
    (consts.CORRECT_INPUT_CSV, consts.CORRECT_INPUT_XLS, consts.CORRECT_INPUT_XLSX),
)
def test_create_data_endpoint_returns_201_created(
    unauthenticated_api_client: APIClientData, file_path: Path
):
    # Given
    client = unauthenticated_api_client.client

    with open(file_path, "rb") as f:
        file_data = SimpleUploadedFile(name=file_path.name, content=f.read())

        # When
        response = client.post(
            get_url("extract-list"), {"file": file_data}, format="multipart"
        )

    # Then
    assert response.status_code == HTTPStatus.OK


def test_create_data_endpoint_returns_422_unprocessable_entity_when_file_not_attached(
    unauthenticated_api_client: APIClientData,
):
    # When
    response = unauthenticated_api_client.client.post(get_url("extract-list"))

    # Then
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_data_endpoint_returns_400_when_extension_not_supported(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    with open(consts.CORRECT_INPUT_CSV, "rb") as f:
        file_data = SimpleUploadedFile(
            name=consts.NOT_SUPPORTED_INPUT.name, content=f.read()
        )

        # When
        response = client.post(
            get_url("extract-list"), {"file": file_data}, format="multipart"
        )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_data_endpoint_returns_400_when_invalid_data(
    unauthenticated_api_client: APIClientData,
):
    # Given
    client = unauthenticated_api_client.client

    with open(consts.INCORRECT_INPUT, "rb") as f:
        file_data = SimpleUploadedFile(
            name=consts.NOT_SUPPORTED_INPUT.name, content=f.read()
        )

        # When
        response = client.post(
            get_url("extract-list"), {"file": file_data}, format="multipart"
        )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
