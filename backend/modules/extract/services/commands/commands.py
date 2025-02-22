from typing import List

import pandas as pd
import pandera as pa

from ....common.domain.exceptions import (
    DataFormatNotSupportedException,
    DataValidationException,
)
from ....data.domain import value_objects as data_value_objects
from ...domain import commands as domain_commands


def extract(command: domain_commands.ExtractData) -> data_value_objects.InputData:
    # 1) validate if file exists
    if not command.file_path.exists():
        raise FileNotFoundError("Input file doesn't exist.")

    # 2) read file according to format
    suffix = command.file_path.suffix
    if suffix == ".csv":
        df = pd.read_csv(command.file_path)
    elif suffix == ".xls" or suffix == ".xlsx":
        df = pd.read_excel(command.file_path)
    else:
        raise DataFormatNotSupportedException(f"Data format {suffix} is not supported.")

    # 3)validate dataframe
    try:
        validated_data: pd.DataFrame = data_value_objects.InputData.validate(df)
    except pa.errors.SchemaError as e:
        raise DataValidationException("Input data is invalid.")

    return validated_data

    # return InputData
