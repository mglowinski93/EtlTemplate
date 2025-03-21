import logging
from typing import cast

import pandas as pd
import pandera as pa

from ....common import const as common_consts
from ....common.domain.exceptions import DataValidationException
from ....data.domain import value_objects as data_value_objects
from ...domain import commands as domain_commands
from ..strategies import AbstractExtraction, choose_strategy

logger = logging.getLogger(__name__)


def extract(command: domain_commands.ExtractData) -> data_value_objects.InputData:
    logger.info(f"Started data extraction from {str(command.file_path.name)}.")
    if not command.file_path.exists():
        raise FileNotFoundError(
            {
                common_consts.ERROR_DETAIL_KEY: f"Input file {str(command.file_path.name)} doesn't exist."
            }
        )

    read_strategy: AbstractExtraction = choose_strategy(command.file_path.suffix)()
    df: pd.DataFrame = read_strategy.read(command.file_path)

    try:
        validated_data = cast(data_value_objects.InputData, data_value_objects.InputData.validate(df))
    except pa.errors.SchemaError:
        raise DataValidationException(
            {
                common_consts.ERROR_DETAIL_KEY: f"Invalid input data in file {str(command.file_path.name)}."
            }
        )

    logger.info(f"Successfully extracted dataset from {str(command.file_path.name)}.")

    return validated_data
