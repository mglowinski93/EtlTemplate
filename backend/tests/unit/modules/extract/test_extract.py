import pandas as pd
import pytest

from modules.extract.domain import commands as domain_commands
from modules.extract.domain.exceptions import (
    DataValidationError,
    FileExtensionNotSupportedError,
)
from modules.extract.services.commands import extract
from tests import test_const 


def test_extract_successfully_read_csv_file():
    # Given
    test_dataset_size = 10
    extract_command = domain_commands.ExtractData(
        file_path=test_const.CORRECT_INPUT_CSV
    )
    # When
    input_data: pd.DataFrame = extract(extract_command)
    # Then
    assert not input_data.empty
    assert input_data.shape[0] == test_dataset_size


def test_extract_successfully_read_xlsx_file():
    # Given
    test_dataset_size = 10
    extract_command = domain_commands.ExtractData(
        file_path=test_const.CORRECT_INPUT_XLSX
    )
    # When
    input_data: pd.DataFrame = extract(extract_command)
    # Then
    assert not input_data.empty
    #todo https://www.w3schools.com/python/ref_func_all.asp
    assert input_data.shape[0] == test_dataset_size


def test_extract_successfully_read_xls_file():
    # Given
    test_dataset_size = 10
    extract_command = domain_commands.ExtractData(
        file_path=test_const.CORRECT_INPUT_XLS
    )
    # When
    input_data: pd.DataFrame = extract(extract_command)
    # Then
    assert not input_data.empty
    #todo https://www.w3schools.com/python/ref_func_all.asp
    #todo verify sources mateusz sent me and compare if anything is missing
    assert input_data.shape[0] == test_dataset_size


def test_extract_raise_exception_when_file_type_is_not_supported():
    # Given
    extract_command = domain_commands.ExtractData(
        file_path=test_const.NOT_SUPPORTED_INPUT
    )

    # When and then
    with pytest.raises(
        FileExtensionNotSupportedError
    ) as err:
        extract(extract_command)


def test_extract_raise_exception_when_any_dataset_row_is_invalid():
    # Given
    extract_command = domain_commands.ExtractData(
        file_path=test_const.INCORRECT_INPUT
    )
    # When and Then
    with pytest.raises(
        DataValidationError,
    ) as err:
        extract(extract_command)
