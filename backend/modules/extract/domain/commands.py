from dataclasses import dataclass
from pathlib import Path

from ...common.domain import commands as common_commands


@dataclass(frozen=True)
class ExtractData(common_commands.DomainCommand):
    file_path: Path
