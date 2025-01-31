import csv
import io
from http import HTTPStatus
from typing import Any

from django.core.files.uploadedfile import SimpleUploadedFile

from infrastructures.apps.common import consts as infrastructure_common_consts
from infrastructures.apps.load.views import serializers

from ... import consts
from ..dtos import APIClientData
from ..utils import get_url


def test_etl_process(unauthenticated_api_client: APIClientData):
    # Given
    client = unauthenticated_api_client.client

    with open(consts.CORRECT_INPUT_CSV, "rb") as _file:
        content = _file.read()
        file_data = SimpleUploadedFile(
            name=consts.CORRECT_INPUT_CSV.name, content=content
        )

        decoded = io.StringIO(content.decode("utf-8"))
        reader = csv.reader(decoded)
        row_count = sum(1 for _ in reader) - 1

        # When
        response = client.post(
            get_url("extract-list"), {"file": file_data}, format="multipart"
        )

    # Then
    assert response.status_code == HTTPStatus.OK

    # When
    response = client.get(get_url("load-list"))

    # Then
    assert response.status_code == HTTPStatus.OK

    json_response: dict[str, Any] = response.data
    assert infrastructure_common_consts.PAGINATION_COUNT_NAME in json_response
    assert (
        json_response[infrastructure_common_consts.PAGINATION_COUNT_NAME] == row_count
    )

    assert infrastructure_common_consts.PAGINATION_RESULTS_NAME in json_response
    results = json_response[infrastructure_common_consts.PAGINATION_RESULTS_NAME]

    # Checking only the data amount is enough. Transformation is tested in unit tests.
    assert isinstance(results, list)
    assert all(
        serializers.OutputDataReadSerializer(data=data).is_valid() for data in results
    )
