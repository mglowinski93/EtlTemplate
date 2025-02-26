from pathlib import Path

import pandas as pd
import pytest

from modules.common.domain.exceptions import (
    DataValidationException,
    FileDataFormatNotSupportedException,
)
from modules.extract.domain import commands as domain_commands
from modules.extract.services.commands import extract


def test_extract_raise_exception_when_file_does_not_exist():
    # Given
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "non_existent_input.csv"
    )
    # When and Then
    with pytest.raises(
        FileNotFoundError,
        match=f"Input file {str(extract_command.file_path.name)} doesn't exist.",
    ):
        extract(extract_command)


def test_extract_raise_exception_when_file_type_is_not_supported():
    # Given
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "not_supported_input.png"
    )
    # When and Then
    with pytest.raises(
        FileDataFormatNotSupportedException, match="Data format .png is not supported."
    ):
        extract(extract_command)


def test_extract_raise_exception_when_any_dataset_row_is_invalid():
    # Given
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "incorrect_data_input.csv"
    )
    # When and Then
    with pytest.raises(
        DataValidationException,
        match=f"Invalid input data in file {str(extract_command.file_path.name)}.",
    ):
        extract(extract_command)


def test_extract_successfully_read_csv_file():
    # Given
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "correct_input.csv"
    )
    # When
    input_data: pd.DataFrame = extract(extract_command)
    # Then
    assert not input_data.empty
    assert input_data.shape[0] == TEST_DATASET_SIZE


def test_extract_successfully_read_xlsx_file():
    # Given
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "correct_input.xlsx"
    )
    # When
    input_data: pd.DataFrame = extract(extract_command)
    # Then
    assert not input_data.empty
    assert input_data.shape[0] == TEST_DATASET_SIZE


def test_extract_successfully_read_xls_file():
    # Given
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "correct_input.xls"
    )
    # When
    input_data: pd.DataFrame = extract(extract_command)
    # Then
    assert not input_data.empty
    assert input_data.shape[0] == TEST_DATASET_SIZE

TEST_DATASET_SIZE = 10
