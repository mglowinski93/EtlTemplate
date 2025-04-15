from dataclasses import dataclass
from datetime import datetime

from ...domain.value_objects import DataId


@dataclass(frozen=True)
class OutputData:
    id: DataId
    full_name: str
    is_satisfied: bool
    timestamp: datetime

@dataclass(frozen=True)
class DetailedOutputData(OutputData):
    age: int

