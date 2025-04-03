import pytest

from modules.extract.domain import commands, value_objects
from modules.extract.domain.exceptions import (
    DataValidationError,
    FileExtensionNotSupportedError,
)
from modules.extract.domain.ports import repositories, units_of_work
from modules.extract.services.commands import extract
from tests import test_const

from ....common.annotations import YieldFixture
from .fakers import (
    TestExtractDomainRepository,
    TestExtractUnitOfWork,
    TestFileDomainRepository,
)


def test_extract_successfully_read_csv_file(
    test_data_unit_of_work: units_of_work.AbstractExtractUnitOfWork,
    test_extract_repository: repositories.AbstractExtractDomainRepository,
    test_file_repository: repositories.AbstractFileDomainRepository,
):
    # Given
    test_dataset_size = 10

    # When
    input_data: value_objects.InputData = extract(
        extract_unit_of_work=test_data_unit_of_work,
        command=commands.ExtractData(
            file=test_const.CORRECT_INPUT_CSV.read_bytes(),
            file_name=test_const.CORRECT_INPUT_CSV.name,
        ),
    )

    # Then
    assert not input_data.empty  # type: ignore[attr-defined]
    assert input_data.shape[0] == test_dataset_size  # type: ignore[attr-defined]
    assert test_file_repository.file_exists(test_const.CORRECT_INPUT_CSV)
    assert len(test_extract_repository.list()) == 1  # type: ignore[attr-defined]
    assert (
        test_extract_repository.list()[0].input_file_name  # type: ignore[attr-defined]
        == test_const.CORRECT_INPUT_CSV.name
    )
    assert (
        test_extract_repository.list()[0].saved_file_name  # type: ignore[attr-defined]
        == test_const.CORRECT_INPUT_CSV.name
    )


def test_extract_successfully_read_xlsx_file(
    test_data_unit_of_work: units_of_work.AbstractExtractUnitOfWork,
    test_extract_repository: repositories.AbstractExtractDomainRepository,
    test_file_repository: repositories.AbstractFileDomainRepository,
):
    # Given
    test_dataset_size = 10

    # When
    input_data: value_objects.InputData = extract(
        extract_unit_of_work=test_data_unit_of_work,
        command=commands.ExtractData(
            file=test_const.CORRECT_INPUT_XLSX.read_bytes(),
            file_name=test_const.CORRECT_INPUT_XLSX.name,
        ),
    )
    # Then
    assert not input_data.empty  # type: ignore[attr-defined]
    assert input_data.shape[0] == test_dataset_size  # type: ignore[attr-defined]
    assert test_file_repository.file_exists(test_const.CORRECT_INPUT_XLSX)
    assert len(test_extract_repository.list()) == 1  # type: ignore[attr-defined]
    assert (
        test_extract_repository.list()[0].input_file_name  # type: ignore[attr-defined]
        == test_const.CORRECT_INPUT_XLSX.name
    )
    assert (
        test_extract_repository.list()[0].saved_file_name  # type: ignore[attr-defined]
        == test_const.CORRECT_INPUT_XLSX.name
    )


def test_extract_successfully_read_xls_file(
    test_data_unit_of_work: units_of_work.AbstractExtractUnitOfWork,
    test_extract_repository: repositories.AbstractExtractDomainRepository,
    test_file_repository: repositories.AbstractFileDomainRepository,
):
    # Given
    test_dataset_size = 10

    # When
    input_data: value_objects.InputData = extract(
        extract_unit_of_work=test_data_unit_of_work,
        command=commands.ExtractData(
            file=test_const.CORRECT_INPUT_XLS.read_bytes(),
            file_name=test_const.CORRECT_INPUT_XLS.name,
        ),
    )
    # Then
    assert not input_data.empty  # type: ignore[attr-defined]
    assert input_data.shape[0] == test_dataset_size  # type: ignore[attr-defined]
    assert test_file_repository.file_exists(test_const.CORRECT_INPUT_XLS)
    assert len(test_extract_repository.list()) == 1  # type: ignore[attr-defined]
    assert (
        test_extract_repository.list()[0].input_file_name  # type: ignore[attr-defined]
        == test_const.CORRECT_INPUT_XLS.name
    )
    assert (
        test_extract_repository.list()[0].saved_file_name  # type: ignore[attr-defined]
        == test_const.CORRECT_INPUT_XLS.name
    )


def test_extract_raise_exception_when_file_type_is_not_supported(
    test_data_unit_of_work: units_of_work.AbstractExtractUnitOfWork,
):
    # Given
    extract_command = commands.ExtractData(
        file=test_const.NOT_SUPPORTED_INPUT.read_bytes(),
        file_name=test_const.NOT_SUPPORTED_INPUT.name,
    )

    # When and then
    with pytest.raises(FileExtensionNotSupportedError):
        extract(extract_unit_of_work=test_data_unit_of_work, command=extract_command)


def test_extract_raise_exception_when_any_dataset_row_is_invalid(
    test_data_unit_of_work: units_of_work.AbstractExtractUnitOfWork,
):
    # Given
    extract_command = commands.ExtractData(
        file=test_const.INCORRECT_INPUT.read_bytes(),
        file_name=test_const.INCORRECT_INPUT.name,
    )

    # When and Then
    with pytest.raises(DataValidationError):
        extract(extract_unit_of_work=test_data_unit_of_work, command=extract_command)


@pytest.fixture
def test_file_repository() -> YieldFixture[TestFileDomainRepository]:
    yield TestFileDomainRepository()


@pytest.fixture
def test_extract_repository() -> YieldFixture[TestExtractDomainRepository]:
    yield TestExtractDomainRepository()


@pytest.fixture
def test_data_unit_of_work(
    test_file_repository, test_extract_repository
) -> YieldFixture[TestExtractUnitOfWork]:
    test_unit_of_work = TestExtractUnitOfWork()
    test_unit_of_work.file = test_file_repository
    test_unit_of_work.extract = test_extract_repository
    yield test_unit_of_work
