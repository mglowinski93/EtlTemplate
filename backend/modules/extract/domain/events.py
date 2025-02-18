from dataclasses import dataclass
from pathlib import Path

from ...common.domain import events as common_events


@dataclass(frozen=True)
class DataExtracted(common_events.DomainEvent):
    file_path: Path
