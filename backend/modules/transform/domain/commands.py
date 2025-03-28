from dataclasses import dataclass

from ...common.domain import commands as common_commands
from ...extract.domain import value_objects as extract_value_objects


@dataclass(frozen=True)
class TransformData(common_commands.DomainCommand):
    data: extract_value_objects.InputData
