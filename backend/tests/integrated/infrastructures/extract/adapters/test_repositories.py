import os

import pytest
from django.core import exceptions as django_exceptions
from django.core.files.storage import FileSystemStorage
from django.db import DatabaseError
from pytest_mock import MockFixture

from infrastructures.apps.common import exceptions as common_exceptions
from infrastructures.apps.extract import exceptions, models
from modules.extract.domain import ports
from tests import consts

from ..fakers import fake_extract_history


def test_django_file_domain_repository_save_method_saves_file(
    tmp_path,
    test_django_file_domain_repository: ports.AbstractFileDomainRepository,
):
    # Given
    with open(consts.CORRECT_INPUT_CSV, "rb") as file:
        file_bytes = file.read()

    # When
    result = test_django_file_domain_repository.save(
        file_name=os.path.basename(consts.CORRECT_INPUT_CSV),
        file=file_bytes,
    )

    # Then
    assert isinstance(result, str)
    assert (tmp_path / result).exists()


@pytest.mark.parametrize(
    "side_effect", (OSError, django_exceptions.SuspiciousFileOperation)
)
def test_django_file_domain_repository_save_method_raises_custom_exception_on_database_exception(
    mocker: MockFixture,
    test_django_file_domain_repository: ports.AbstractFileDomainRepository,
    side_effect,
):
    # Given
    with open(consts.INCORRECT_INPUT, "rb") as file:
        file_bytes = file.read()

    mocker.patch.object(FileSystemStorage, "save", side_effect=side_effect)

    # When and then
    with pytest.raises(exceptions.FileSaveError):
        test_django_file_domain_repository.save(
            file_name=os.path.basename(consts.INCORRECT_INPUT),
            file=file_bytes,
        )


def test_django_extract_domain_repository_create_method_creates_record(
    test_django_extract_domain_repository: ports.AbstractExtractDomainRepository,
):
    # Given
    extract_history = fake_extract_history()

    # When
    test_django_extract_domain_repository.create(extract_history)

    # Then
    assert models.ExtractHistory.objects.filter(
        input_file_name=extract_history.input_file_name
    ).exists()


def test_django_extract_domain_repository_create_method_raises_custom_exception_on_database_exception(
    mocker: MockFixture,
    test_django_extract_domain_repository: ports.AbstractExtractDomainRepository,
):
    # Given
    extract_history = fake_extract_history()

    side_effect = DatabaseError
    mocker.patch.object(
        models.ExtractHistory.objects,
        "create",
        side_effect=side_effect,
    )
    
    # When and then
    with pytest.raises(common_exceptions.DatabaseError):
        test_django_extract_domain_repository.create(extract_history)
    assert not models.ExtractHistory.objects.exists()
