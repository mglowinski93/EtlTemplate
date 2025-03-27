from dataclasses import dataclass

from ...common.domain import commands as common_commands
from ...transform.domain import value_objects as domain_value_objects


@dataclass(frozen=True)
class SaveData(common_commands.DomainCommand):
    output_data: list[domain_value_objects.OutputData]
