from dataclasses import dataclass

from ...common.domain import commands as common_commands
from ...load.services import queries as load_queries


@dataclass(frozen=True)
class SaveData(common_commands.DomainCommand):
    output_data: list[load_queries.OutputData]
