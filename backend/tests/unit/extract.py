from pathlib import Path

import pandas as pd
import pytest
from modules.common.domain.exceptions import (
    DataValidationException,
    FileDataFormatNotSupportedException,
)
from modules.extract.domain import commands as domain_commands
from modules.extract.services.commands import commands as service_commands


def test_extract_raise_exception_when_file_does_not_exist():
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "non_existent_input.csv"
    )
    with pytest.raises(FileNotFoundError, match="Input file doesn't exist."):
        service_commands.extract(extract_command)


def test_extract_raise_exception_when_file_type_is_not_supported():
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "not_supported_input.png"
    )
    with pytest.raises(
        FileDataFormatNotSupportedException, match="Data format .png is not supported."
    ):
        service_commands.extract(extract_command)


def test_extract_raise_exception_when_any_dataset_row_is_invalid():
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "incorrect_data_input.csv"
    )

    with pytest.raises(DataValidationException, match="Input data is invalid."):
        service_commands.extract(extract_command)


def test_extract_successfully_read_csv_file():
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "correct_input.csv"
    )
    input_data: pd.DataFrame = service_commands.extract(extract_command)
    assert not input_data.empty
    assert input_data.shape[0] == 10


def test_extract_successfully_read_xlsx_file():
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "correct_input.xlsx"
    )
    input_data: pd.DataFrame = service_commands.extract(extract_command)
    assert not input_data.empty
    assert input_data.shape[0] == 10


def test_extract_successfully_read_xls_file():
    extract_command = domain_commands.ExtractData(
        file_path=Path(__file__).parent / "resources" / "correct_input.xls"
    )
    input_data: pd.DataFrame = service_commands.extract(extract_command)
    assert not input_data.empty
    assert input_data.shape[0] == 10
