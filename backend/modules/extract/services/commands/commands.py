import logging
from datetime import datetime
from pathlib import Path
from typing import cast

import pandas as pd
import pandera as pa

from ...domain.commands import ExtractData
from ...domain.exceptions import DataValidationError
from ...domain.ports.units_of_work import AbstractExtractUnitOfWork
from ...domain.value_objects import ExtractHistory, InputData
from ..strategies import AbstractExtraction, choose_strategy

logger = logging.getLogger(__name__)


def extract(
    extract_unit_of_work: AbstractExtractUnitOfWork, command: ExtractData
) -> InputData:
    with extract_unit_of_work:
        logger.info("Saving file...")
        saved_file_name: str = extract_unit_of_work.file.save(
            file=command.file, file_name=command.file_name
        )
        logger.info("File saved.")

        logger.info("Saving extract history...")
        extract_unit_of_work.extract.create(
            ExtractHistory(
                input_file_name=command.file_name,
                saved_file_name=saved_file_name,
                timestamp=datetime.now(),
            )
        )
        logger.info("Extract history saved.")

    logger.info("Started data extraction.")
    read_strategy: AbstractExtraction = choose_strategy(
        Path(command.file_name).suffix
    )()
    df: pd.DataFrame = read_strategy.read(command.file)
    try:
        validated_data = cast(InputData, InputData.validate(df))
    except pa.errors.SchemaError as err:
        raise DataValidationError(
            message=f"Invalid input data in file {saved_file_name}",
            file_name=saved_file_name,
        ) from err

    logger.info("Dataset extracted successfully.")

    return validated_data
