import logging
from typing import cast

import pandas as pd
import pandera as pa

from ....common.domain import exceptions as domain_exceptions
from ....data.domain import value_objects as data_value_objects
from ...domain import commands as domain_commands
from ..strategies import AbstractExtraction, choose_strategy

logger = logging.getLogger(__name__)


def extract(command: domain_commands.ExtractData) -> data_value_objects.InputData:
    logger.info(f"Started data extraction from {command.file_path.name}.")
    if not command.file_path.exists():
        raise domain_exceptions.FileNotFoundError(
            message="File %s not found", file_name=command.file_path.name
        )

    read_strategy: AbstractExtraction = choose_strategy(command.file_path.suffix)()
    df: pd.DataFrame = read_strategy.read(command.file_path)

    try:
        validated_data = cast(
            data_value_objects.InputData, data_value_objects.InputData.validate(df)
        )
    except pa.errors.SchemaError:
        raise domain_exceptions.DataValidationError(
            message="Invalid input data in file %s", file_name=command.file_path.name
        )

    logger.info(f"Successfully extracted dataset from {command.file_path.name}.")

    return validated_data
