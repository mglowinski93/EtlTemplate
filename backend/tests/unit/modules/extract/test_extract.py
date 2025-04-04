import pytest

from modules.extract.domain import commands, value_objects
from modules.extract.domain import exceptions as domain_exceptions
from modules.extract.domain import ports
from modules.extract.services.commands import extract
from tests import test_const


def test_extract_successfully_read_csv_file(
    test_extract_unit_of_work: ports.AbstractExtractUnitOfWork
):
    # When
    input_data: value_objects.InputData = extract(
        extract_unit_of_work=test_extract_unit_of_work,
        command=commands.ExtractData(
            file=test_const.CORRECT_INPUT_CSV.read_bytes(),
            file_name=test_const.CORRECT_INPUT_CSV.name,
        ),
    )

    # Then
    assert not input_data.empty  # type: ignore[attr-defined]
    assert len(input_data)== test_const.DATASET_INPUT_SIZE  # type: ignore[attr-defined]

    assert test_extract_unit_of_work.file.file_exists(test_const.CORRECT_INPUT_CSV)

    extract_history_results = test_extract_unit_of_work.extract.list()
    assert len(extract_history_results) == 1 
    assert all(extract_history.input_file_name == test_const.CORRECT_INPUT_CSV.name
        for extract_history in extract_history_results
    )
    assert all(extract_history.saved_file_name == test_const.CORRECT_INPUT_CSV.name
        for extract_history in extract_history_results
    )


def test_extract_successfully_read_xlsx_file(
    test_extract_unit_of_work: ports.AbstractExtractUnitOfWork
):
    # When
    input_data: value_objects.InputData = extract(
        extract_unit_of_work=test_extract_unit_of_work,
        command=commands.ExtractData(
            file=test_const.CORRECT_INPUT_XLSX.read_bytes(),
            file_name=test_const.CORRECT_INPUT_XLSX.name,
        ),
    )
    # Then
    assert not input_data.empty  # type: ignore[attr-defined]
    assert len(input_data) == test_const.DATASET_INPUT_SIZE  # type: ignore[attr-defined]

    assert test_extract_unit_of_work.file.file_exists(test_const.CORRECT_INPUT_XLSX)

    extract_history_results = test_extract_unit_of_work.extract.list()
    assert len(extract_history_results) == 1 
    assert all(extract_history.input_file_name == test_const.CORRECT_INPUT_XLSX.name
        for extract_history in extract_history_results
    )
    assert all(extract_history.saved_file_name == test_const.CORRECT_INPUT_XLSX.name
        for extract_history in extract_history_results
    )


def test_extract_successfully_read_xls_file(
    test_extract_unit_of_work: ports.AbstractExtractUnitOfWork
):
    # When
    input_data: value_objects.InputData = extract(
        extract_unit_of_work=test_extract_unit_of_work,
        command=commands.ExtractData(
            file=test_const.CORRECT_INPUT_XLS.read_bytes(),
            file_name=test_const.CORRECT_INPUT_XLS.name,
        ),
    )
    # Then
    assert not input_data.empty  # type: ignore[attr-defined]
    assert len(input_data) == test_const.DATASET_INPUT_SIZE  # type: ignore[attr-defined]

    assert test_extract_unit_of_work.file.file_exists(test_const.CORRECT_INPUT_XLS)

    extract_history_results = test_extract_unit_of_work.extract.list()
    assert len(extract_history_results) == 1 
    assert all(extract_history.input_file_name == test_const.CORRECT_INPUT_XLS.name
        for extract_history in extract_history_results
    )
    assert all(extract_history.saved_file_name == test_const.CORRECT_INPUT_XLS.name
        for extract_history in extract_history_results
    )

def test_extract_raise_exception_when_file_type_is_not_supported(
    test_extract_unit_of_work: ports.AbstractExtractUnitOfWork
):
    # Given
    extract_command = commands.ExtractData(
        file=test_const.NOT_SUPPORTED_INPUT.read_bytes(),
        file_name=test_const.NOT_SUPPORTED_INPUT.name,
    )

    # When and then
    with pytest.raises(domain_exceptions.FileExtensionNotSupportedError):
        extract(extract_unit_of_work=test_extract_unit_of_work, command=extract_command)


def test_extract_raise_exception_when_any_dataset_row_is_invalid(
    test_extract_unit_of_work: ports.AbstractExtractUnitOfWork
):
    # Given
    extract_command = commands.ExtractData(
        file=test_const.INCORRECT_INPUT.read_bytes(),
        file_name=test_const.INCORRECT_INPUT.name,
    )

    # When and Then
    with pytest.raises(domain_exceptions.DataValidationError):
        extract(extract_unit_of_work=test_extract_unit_of_work, command=extract_command)

