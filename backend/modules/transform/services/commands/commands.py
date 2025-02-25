import logging

import pandas as pd

from ...domain import commands as domain_commands

logger = logging.getLogger(__name__)


def transform(command: domain_commands.TransformData):
    logger.info("Data transformation start.")
    df: pd.DataFrame = command.data
    df["full_name"] = df["name"] + " " + df["surname"]
    df.drop(columns=["name", "surname"])
    logger.info("Data transformation done.")
    return df
