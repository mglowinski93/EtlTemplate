from dataclasses import dataclass

from ...data.domain import commands as common_commands
from ...data.domain import value_objects as data_value_objects


@dataclass(frozen=True)
class TransformData(common_commands.DomainCommand):
    input_data: data_value_objects.InputData
