import logging

import pandas as pd

from ...domain import commands as domain_commands
from ....data.domain import value_objects as data_value_objects

logger = logging.getLogger(__name__)


def transform(command: domain_commands.TransformData) -> list[data_value_objects.OutputData]:
    logger.info("Data transformation start.")
    df: pd.DataFrame = command.data
    df["full_name"] = df["name"] + " " + df["surname"]
    df = df.drop(columns=["name", "surname"])
    transformation_result = [data_value_objects.OutputData(**record) for record in df.to_dict(orient="records")]
    logger.info("Data transformation done.")
    return transformation_result
