import logging

import pandas as pd
import pandera as pa
from pandera.typing.pandas import DataFrame

from ....common.domain.exceptions import DataValidationException
from ....data.domain import value_objects as data_value_objects
from ...domain import commands as domain_commands
from ..strategies import AbstractExtraction, choose_strategy

logger = logging.getLogger(__name__)


def extract(
    command: domain_commands.ExtractData,
) -> DataFrame[data_value_objects.InputData]:
    logger.info(f"Started data extraction from {str(command.file_path.name)}.")
    if not command.file_path.exists():
        raise FileNotFoundError(
            f"Input file {str(command.file_path.name)} doesn't exist."
        )

    read_strategy: AbstractExtraction = choose_strategy(command.file_path.suffix)()

    data: pd.DataFrame = read_strategy.read(command.file_path)

    try:
        validated_data = data_value_objects.InputData.validate(data)
    except pa.errors.SchemaError:
        logger.info(f"Invalid input data in file {str(command.file_path.name)}.")
        raise DataValidationException(
            f"Invalid input data in file {str(command.file_path.name)}."
        )

    logger.info(f"Successfully extracted dataset from {str(command.file_path.name)}.")

    return validated_data  # type: ignore[return-value]
