import pandas as pd
import pandera as pa

from ....common.domain.exceptions import DataValidationException
from ....data.domain import value_objects as data_value_objects
from ...domain import commands as domain_commands
from ..strategies import read_strategies


def extract(command: domain_commands.ExtractData) -> data_value_objects.InputData:
    if not command.file_path.exists():
        raise FileNotFoundError("Input file doesn't exist.")

    read_strategy: read_strategies.AbstractRead = read_strategies.choose_strategy(
        command.file_path.suffix
    )()

    df: pd.DataFrame = read_strategy.read(command.file_path)

    try:
        validated_data: data_value_objects.InputData = (
            data_value_objects.InputData.validate(df)
        )
    except pa.errors.SchemaError:
        raise DataValidationException("Input data is invalid.")

    return validated_data.df
