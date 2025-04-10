import os
from datetime import datetime

import pytest
from django.core import exceptions as django_exceptions
from django.core.files.storage import FileSystemStorage
from django.db import DatabaseError
from pytest_mock import MockFixture

from infrastructures.apps.common import exceptions as common_exceptions
from infrastructures.apps.extract import exceptions, models
from modules.extract.domain import ports, value_objects
from tests import const


def test_django_file_domain_repository_save_method_saves_file(
    tmp_path,
    test_django_file_domain_repository: ports.AbstractFileDomainRepository,
):
    # Given
    with open(const.CORRECT_INPUT_CSV, "rb") as file:
        file_bytes = file.read()

    # When
    result = test_django_file_domain_repository.save(
        file_name=os.path.basename(const.CORRECT_INPUT_CSV),
        file=file_bytes,
        location=str(tmp_path),
    )

    # Then
    assert isinstance(result, str)
    assert (tmp_path / result).exists()


def test_django_file_domain_repository_save_method_raises_custom_exception_on_django_exception(
    tmp_path,
    mocker: MockFixture,
    test_django_file_domain_repository: ports.AbstractFileDomainRepository,
):
    # Given
    with open(const.INCORRECT_INPUT, "rb") as file:
        file_bytes = file.read()

    side_effect = OSError
    mocker.patch.object(FileSystemStorage, "save", side_effect=side_effect)

    # When and Then
    with pytest.raises(exceptions.FileSaveError):
        test_django_file_domain_repository.save(
            file_name=os.path.basename(const.INCORRECT_INPUT),
            file=file_bytes,
            location=str(tmp_path),
        )


def test_django_file_domain_repository_save_method_raises_file_save_error_on_suspicious_file_error(
    tmp_path,
    mocker: MockFixture,
    test_django_file_domain_repository: ports.AbstractFileDomainRepository,
):
    # Given
    with open(const.INCORRECT_INPUT, "rb") as file:
        file_bytes = file.read()

    side_effect = django_exceptions.SuspiciousFileOperation
    mocker.patch.object(FileSystemStorage, "save", side_effect=side_effect)

    # When and Then
    with pytest.raises(exceptions.FileSaveError):
        test_django_file_domain_repository.save(
            file_name=os.path.basename(const.INCORRECT_INPUT),
            file=file_bytes,
            location=str(tmp_path),
        )


def test_django_extract_domain_repository_create_method_creates_record(
    test_django_extract_domain_repository: ports.AbstractExtractDomainRepository,
):
    # Given
    extract_history_entity = value_objects.ExtractHistory(
        "test_file.csv", "saved_file.csv", timestamp=datetime.now()
    )

    # When
    test_django_extract_domain_repository.create(extract_history_entity)

    # Then
    assert (
        models.ExtractHistory.objects.filter(
            input_file_name=extract_history_entity.input_file_name
        ).exists()
    )


def test_django_extract_domain_repository_create_method_raises_custom_exception_on_django_exception(
    mocker: MockFixture,
    test_django_extract_domain_repository: ports.AbstractExtractDomainRepository,
):
    # Given
    extract_history_entity = value_objects.ExtractHistory(
        "test_file.csv", "saved_file.csv", timestamp=datetime.now()
    )

    side_effect = DatabaseError

    mocker.patch(
        "infrastructures.apps.extract.models.ExtractHistory.objects.create",
        side_effect=side_effect,
    )
    # When and Then
    with pytest.raises(common_exceptions.DatabaseError):
        test_django_extract_domain_repository.create(extract_history_entity)
