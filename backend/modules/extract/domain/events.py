from dataclasses import dataclass
from pathlib import Path
from ...common.domain.events import DomainEvent


@dataclass(frozen=True)
class DataExtracted(DomainEvent):
    file_path: Path
