import logging
from typing import cast

import pandas as pd

from ....load.services import queries as load_queries
from ...domain import commands as domain_commands

logger = logging.getLogger(__name__)


def transform(
    command: domain_commands.TransformData,
) -> list[load_queries.OutputData]:
    logger.info("Data transformation start.")

    df: pd.DataFrame = cast(pd.DataFrame, command.data)
    df["full_name"] = pd.concat([df["name"], df["surname"]], axis=1).agg(
        " ".join, axis=1
    )
    df.drop(columns=["name", "surname"], inplace=True)
    transformation_result = [
        load_queries.OutputData(
            record["full_name"], record["age"], record["is_satisfied"]
        )
        for record in df.to_dict(orient="records")
    ]

    logger.info("Data transformation done.")

    return transformation_result
