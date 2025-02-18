from dataclasses import dataclass
from pathlib import Path

from ...data.domain.events import DomainEvent


# TODO: discuss what kind of information we want to pass here.
@dataclass(frozen=True)
class DataExtracted(DomainEvent):
    file_path: Path
