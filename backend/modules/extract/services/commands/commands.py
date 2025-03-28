import logging
from typing import cast

import pandas as pd
import pandera as pa

from ...domain import commands as domain_commands
from ...domain import exceptions as extract_exceptions
from ...domain import value_objects
from ..strategies import AbstractExtraction, choose_strategy

logger = logging.getLogger(__name__)


def extract(command: domain_commands.ExtractData) -> value_objects.InputData:
    logger.info("Started data extraction.")
    if not command.file_path.exists():
        logger.error(
            "File containing input data '%s' does not exist.", command.file_path.name
        )
        raise FileNotFoundError(f"Input Data file {command.file_path.name} not found.")

    read_strategy: AbstractExtraction = choose_strategy(command.file_path.suffix)()
    df: pd.DataFrame = read_strategy.read(command.file_path)

    try:
        validated_data = cast(
            value_objects.InputData, value_objects.InputData.validate(df)
        )
    except pa.errors.SchemaError as err:
        raise extract_exceptions.DataValidationError(
            message=f"Invalid input data in file {command.file_path.name}",
            file_name=command.file_path.name,
        ) from err

    logger.info("Dataset extracted successfully.")

    return validated_data
