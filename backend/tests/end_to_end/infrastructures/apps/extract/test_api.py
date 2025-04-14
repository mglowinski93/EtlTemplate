from ....dtos import APIClientData
from django.core.files.uploadedfile import SimpleUploadedFile
from tests import consts
from http import HTTPStatus
from django.urls import reverse
import pytest
from pathlib import Path

@pytest.mark.parametrize(
    "test_file_path", (consts.CORRECT_INPUT_CSV, consts.CORRECT_INPUT_XLS, consts.CORRECT_INPUT_XLSX)
)
def test_create_data_endpoint_returns_201_created(
    unauthenticated_client: APIClientData,
    test_file_path: Path
):
    # Given
    with open(test_file_path, "rb") as f:
        file_data = SimpleUploadedFile(
            name=test_file_path.name,
            content=f.read(),
            content_type="text/csv"
        )

        # When
        response = unauthenticated_client.client.post(
            reverse("extract-list"),
            {"file": file_data},
            format="multipart"
        )

    # Then
    assert response.status_code == HTTPStatus.CREATED


def test_create_data_endpoint_returns_422_unprocessable_entity_when_file_not_attached(
    unauthenticated_client: APIClientData,
):
     # When
    response = unauthenticated_client.client.post(
        reverse("extract-list")
    )

    # Then
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def test_create_data_endpoint_returns_400_when_extension_not_supported(
    unauthenticated_client: APIClientData,
):
    # Given
    with open(consts.CORRECT_INPUT_CSV, "rb") as f:
        file_data = SimpleUploadedFile(
            name=consts.NOT_SUPPORTED_INPUT.name,
            content=f.read(),
            content_type="text/csv"
        )

        # When
        response = unauthenticated_client.client.post(
            reverse("extract-list"),
            {"file": file_data},
            format="multipart"
        )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_data_endpoint_returns_400_when_invalid_data(
    unauthenticated_client: APIClientData,
):
    # Given
    with open(consts.INCORRECT_INPUT, "rb") as f:
        file_data = SimpleUploadedFile(
            name=consts.NOT_SUPPORTED_INPUT.name,
            content=f.read(),
            content_type="text/csv"
        )

        # When
        response = unauthenticated_client.client.post(
            reverse("extract-list"),
            {"file": file_data},
            format="multipart"
        )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
