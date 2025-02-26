from dataclasses import dataclass

from pandera.typing.pandas import DataFrame

from ...common.domain import commands as common_commands
from ...data.domain import value_objects as data_value_objects


@dataclass(frozen=True)
class TransformData(common_commands.DomainCommand):
    data: DataFrame[data_value_objects.InputData]
