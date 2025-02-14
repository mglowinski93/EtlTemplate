from dataclasses import dataclass

from ...common.domain import commands as common_commands
from ...data.domain import value_objects as data_value_objects


@dataclass(frozen=True)
class PersistData(common_commands.DomainCommand):
    output_data: data_value_objects.OutputData
