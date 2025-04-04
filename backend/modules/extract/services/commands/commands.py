import logging
from datetime import datetime
from typing import cast
from pathlib import Path

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
        if not extract_unit_of_work.file.file_exists(saved_file_name):
            logger.error(
                "File containing input data '%s' does not exist.", saved_file_name
            )
            raise FileNotFoundError(
                f"Input Data file {saved_file_name} not found."
            )
    read_strategy: AbstractExtraction = choose_strategy(Path(saved_file_name).suffix)()
    df: pd.DataFrame = read_strategy.read(saved_file_name)
    try:
        validated_data = cast(InputData, InputData.validate(df))
    except pa.errors.SchemaError as err:
        raise DataValidationError(
            message=f"Invalid input data in file {saved_file_name}",
            file_name=saved_file_name,
        ) from err

    logger.info("Dataset extracted successfully.")

    return validated_data
