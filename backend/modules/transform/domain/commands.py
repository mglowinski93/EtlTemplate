from dataclasses import dataclass

import pandas as pd

from ...common.domain import commands as common_commands


@dataclass(frozen=True)
class TransformData(common_commands.DomainCommand):
    data: pd.DataFrame
