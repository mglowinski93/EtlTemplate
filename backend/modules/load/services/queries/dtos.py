from dataclasses import dataclass
from datetime import datetime
from ...domain.value_objects import DataId

@dataclass(frozen=True)
class OutputData:
    id: DataId
    full_name: str
    age: int
    is_satisfied: bool


@dataclass(frozen=True)
class DetailedOutputData(OutputData):
    timestamp: datetime #todo think about where to take it from ? extract history too I believe
