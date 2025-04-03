from dataclasses import dataclass

from ...common.domain import commands as common_commands


@dataclass(frozen=True)
class ExtractData(common_commands.DomainCommand):
    file: bytes
    file_name: str
