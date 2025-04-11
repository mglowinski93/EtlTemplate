import logging
from typing import cast

import pandas as pd

from ...domain.commands import TransformData
from ...domain.value_objects import TransformedData

logger = logging.getLogger(__name__)


def transform(
    command: TransformData,
) -> list[TransformedData]:
    logger.info("Data transformation start.")

    df: pd.DataFrame = cast(pd.DataFrame, command.data)
    df["full_name"] = pd.concat([df["name"], df["surname"]], axis=1).agg(
        " ".join, axis=1
    )
    df.drop(columns=["name", "surname"], inplace=True)
    transformation_result = [
        TransformedData(
            full_name=record["full_name"],
            age=record["age"],
            is_satisfied=record["is_satisfied"],
        )
        for record in df.to_dict(orient="records")
    ]

    logger.info("Data transformation done.")

    return transformation_result
